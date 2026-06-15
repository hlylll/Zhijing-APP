# train.py
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
from torch.optim import AdamW  # 注意这里
import numpy as np
from sklearn.model_selection import train_test_split
import os

# 或者使用阿里源
os.environ['HF_ENDPOINT'] = 'https://mirrors.aliyun.com/huggingface'
# 1. 加载数据
def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    texts = []
    behaviors = []
    labels = []
    
    for item in data:
        texts.append(item['text'])
        beh = item['behavior']
        behaviors.append([
            beh['duration'],
            beh['click_count'],
            beh['delete_count'],
            beh['selected_mood'],
            beh['treehole'],
            beh['streak_days'],
            beh['hour'],
            beh['daily_count']
        ])
        # 标签从1-6转为0-5
        labels.append(item['label'] - 1)
    
    return texts, behaviors, labels

# 2. 数据集类
class MoodDataset(Dataset):
    def __init__(self, texts, behaviors, labels, tokenizer, max_len=128):
        self.texts = texts
        self.behaviors = torch.FloatTensor(behaviors)
        self.labels = torch.LongTensor(labels)
        self.tokenizer = tokenizer
        self.max_len = max_len
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'behavior': self.behaviors[idx],
            'label': self.labels[idx]
        }

# 3. 模型定义
class MoodModel(torch.nn.Module):
    def __init__(self, bert_model, behav_dim=8, hidden_size=768, num_classes=6):
        super().__init__()
        self.bert = bert_model
        self.behav_net = torch.nn.Sequential(
            torch.nn.Linear(behav_dim, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, hidden_size)
        )
        self.classifier = torch.nn.Linear(hidden_size, num_classes)
    
    def forward(self, input_ids, attention_mask, behavior):
        text_embeds = self.bert.embeddings(input_ids)
        behav_vec = self.behav_net(behavior)
        behav_vec = behav_vec.unsqueeze(1)
        combined = torch.cat([behav_vec, text_embeds], dim=1)
        behav_mask = torch.ones(behavior.size(0), 1).to(attention_mask.device)
        combined_mask = torch.cat([behav_mask, attention_mask], dim=1)
        outputs = self.bert(inputs_embeds=combined, attention_mask=combined_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]
        logits = self.classifier(cls_output)
        return logits

# 4. 训练函数
def main():
    print("开始加载数据...")
    texts, behaviors, labels = load_data('training_data.json')
    print(f"加载了 {len(texts)} 条数据")
    
    # 划分训练集和验证集
    train_texts, val_texts, train_behav, val_behav, train_labels, val_labels = train_test_split(
        texts, behaviors, labels, test_size=0.2, random_state=42
    )
    
    # 初始化tokenizer
    tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese')
    
    # 创建数据集
    train_dataset = MoodDataset(train_texts, train_behav, train_labels, tokenizer)
    val_dataset = MoodDataset(val_texts, val_behav, val_labels, tokenizer)
    
    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4)
    
    # 初始化模型
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"使用设备: {device}")
    
    bert = BertModel.from_pretrained('./bert-base-chinese')
    model = MoodModel(bert).to(device)
    
    # 优化器 - 使用 torch.optim.AdamW
    optimizer = AdamW(model.parameters(), lr=2e-5)
    criterion = torch.nn.CrossEntropyLoss()
    
    # 训练
    print("开始训练...")
    best_acc = 0
    
    for epoch in range(15):
        # 训练阶段
        model.train()
        train_loss = 0
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            behavior = batch['behavior'].to(device)
            labels = batch['label'].to(device)
            
            optimizer.zero_grad()
            logits = model(input_ids, attention_mask, behavior)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # 验证阶段
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                behavior = batch['behavior'].to(device)
                labels = batch['label'].to(device)
                
                logits = model(input_ids, attention_mask, behavior)
                preds = torch.argmax(logits, dim=1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)
        
        accuracy = correct / total if total > 0 else 0
        print(f'Epoch {epoch+1}, Loss: {train_loss/len(train_loader):.4f}, Acc: {accuracy:.4f}')
        
        # 保存最佳模型
        if accuracy > best_acc:
            best_acc = accuracy
            # 创建emotion_model文件夹（如果不存在）
            os.makedirs('emotion_model', exist_ok=True)
            torch.save(model.state_dict(), 'emotion_model/best_mood_model.pth')
            tokenizer.save_pretrained('emotion_model/tokenizer')
            print(f'   ✓ 保存最佳模型，准确率: {accuracy:.4f}')
    
    print(f"\n训练完成！最佳准确率: {best_acc:.4f}")
    print("模型已保存到 emotion_model/best_mood_model.pth")

if __name__ == '__main__':
    main()