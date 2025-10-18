import os
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# Создание FastAPI приложения
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    # Загружаем метрики из файла
    try:
        with open('model/metrics.pkl', 'rb') as metrics_file:
            metrics = pickle.load(metrics_file)
    except FileNotFoundError:
        return HTMLResponse("<h1>Метрики не найдены. Пожалуйста, сначала обучите модель.</h1>")

    # Составляем строку с метриками
    metrics_str = f"""
    <h1>Метрики модели Симпсонов</h1>
    <ul>
        <li>Обучение (Training Loss): {metrics['train_loss']:.4f}</li>
        <li>Обучение (Training Accuracy): {metrics['train_accuracy']:.2%}</li>
        <li>Валидация (Validation Loss): {metrics['val_loss']:.4f}</li>
        <li>Валидация (Validation Accuracy): {metrics['val_accuracy']:.2%}</li>
        <li>F1 Score: {metrics['f1_score']:.4f}</li>
    </ul>
    """

    content = f"""
    <html>
        <head>
            <title>Метрики модели Симпсонов</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                li {{
                    margin: 5px 0;
                    font-size: 1.2em;
                }}
            </style>
        </head>
        <body>
            {metrics_str}
        </body>
    </html>
    """

    return HTMLResponse(content=content)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)