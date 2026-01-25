# Запуск
docker build -t mock-api .
docker run -d -p 8000:8000 --name mock-api mock-api

# Запуск тестов (QA)
```bash
docker exec container_name pytest
```
# Проверка после деплоя
```bash
curl http://localhost:8000/order
curl http://localhost:8000/user  
curl http://localhost:8000/catalog | jq '.[0]'
```
