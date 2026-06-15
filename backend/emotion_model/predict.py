# emotion_model/predict.py
import torch
from transformers import BertTokenizer, BertModel
import os
import json

# 模型定义（必须和训练时完全一致）
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

# 全局变量（模型只加载一次）
_model = None
_tokenizer = None
_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    """加载训练好的模型"""
    global _model, _tokenizer
    
    if _model is None:
        print("正在加载情绪识别模型...")
        
        # 使用本地下载的BERT模型
        bert = BertModel.from_pretrained('./bert-base-chinese')
        _tokenizer = BertTokenizer.from_pretrained('./bert-base-chinese')
        
        # 加载训练好的权重
        _model = MoodModel(bert)
        model_path = os.path.join(os.path.dirname(__file__), 'best_mood_model.pth')
        _model.load_state_dict(torch.load(model_path, map_location=_device))
        _model.to(_device)
        _model.eval()
        
        print("✅ 模型加载成功！")
    
    return _model, _tokenizer

# 情绪映射（和您前端保持一致）
mood_map = {
    0: {'id': 1, 'name': '🌈 闪闪发光', 'emoji': '🌻', 'title': '向日葵时刻'},
    1: {'id': 2, 'name': '🌻 温暖生长', 'emoji': '🍃', 'title': '微风日记'},
    2: {'id': 3, 'name': '🎐 微风思绪', 'emoji': '💭', 'title': '思考云朵'},
    3: {'id': 4, 'name': '☔ 雨滴心情', 'emoji': '☁️', 'title': '雨过天晴'},
    4: {'id': 5, 'name': '🎪 马戏团日', 'emoji': '⚡', 'title': '能量爆发'},
    5: {'id': 6, 'name': '🧩 拼图时刻', 'emoji': '🧩', 'title': '拼图时刻'}
}

# 分析文本（根据情绪）
insights = {
    0: "发现3个快乐小种子，继续浇灌它们吧",
    1: "思绪如溪流般清澈，保持这份宁静",
    2: "深度思考让心灵更丰富，已在成长路径上",
    3: "倾诉让心情减轻了30%，明天会更好",
    4: "热情正在燃烧，记得适当休息",
    5: "困惑是成长的前奏，慢慢来"
}

suggestions = {
    0: "对着镜子说一句'今天我也很棒'",
    1: "闭眼倾听周围3种声音",
    2: "用不同颜色标注今天的思绪",
    3: "给自己泡一杯温暖的茶",
    4: "把今天的能量分享给一个人",
    5: "把问题拆解成小部分，逐个解决"
}

tags = {
    0: ['阳光', '能量', '绽放'],
    1: ['平和', '清晰', '自然'],
    2: ['思考', '成长', '探索'],
    3: ['释放', '勇气', '希望'],
    4: ['活力', '热情', '行动'],
    5: ['探索', '思考', '突破']
}

def predict_mood(text, behavior):
    """预测情绪"""
    model, tokenizer = load_model()
    
    # 处理文本
    encoding = tokenizer(
        text,
        truncation=True,
        padding='max_length',
        max_length=128,
        return_tensors='pt'
    )
    input_ids = encoding['input_ids'].to(_device)
    attention_mask = encoding['attention_mask'].to(_device)
    
    # 处理行为数据
    behav_tensor = torch.FloatTensor([[
        behavior['duration'],
        behavior['click_count'],
        behavior['delete_count'],
        behavior['selected_mood'],
        behavior['treehole'],
        behavior['streak_days'],
        behavior['hour'],
        behavior['daily_count']
    ]]).to(_device)
    
    # 预测
    with torch.no_grad():
        logits = model(input_ids, attention_mask, behav_tensor)
        pred = torch.argmax(logits, dim=1).item()
    
    # 返回结果
    result = mood_map[pred]
    return {
        'success': True,
        'mood_id': result['id'],
        'mood_name': result['name'],
        'emoji': result['emoji'],
        'title': result['title'],
        'insight': insights[pred],
        'suggestion': suggestions[pred],
        'tags': tags[pred]
    }

# 测试函数
if __name__ == '__main__':
    # 测试预测
    test_text = "今天好开心啊，拿到了offer！"
    test_behavior = {
        'duration': 120,
        'click_count': 5,
        'delete_count': 1,
        'selected_mood': 1,
        'treehole': 0,
        'streak_days': 7,
        'hour': 14,
        'daily_count': 1
    }
    
    result = predict_mood(test_text, test_behavior)
    print("预测结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))