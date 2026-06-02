# Документация Self Core Java

Этот каталог содержит структурированную русскоязычную документацию по системе Self Core Java.

## Основные обзорные документы

- [Описание системы для заказчика](/D:/project/Self_core_java/docs/system-description-ru.md)
- [Матрица трассировки функций](/D:/project/Self_core_java/docs/functional-traceability-matrix-ru.md)
- [Правила сопровождения документации](/D:/project/Self_core_java/docs/documentation-rules.md)
- [Памятка по безопасной работе с русскими файлами](/D:/project/Self_core_java/docs/russian-text-safety-guide.md)

## Demo

- [Ответы на демонстрационный опросник](/D:/project/Self_core_java/docs/demo/demo-questionnaire-answers-ru.md)
- [План проверки и доработок](/D:/project/Self_core_java/docs/demo/demo-gap-plan-ru.md)

## Разделы

### 1. Архитектура
- [Обзор раздела архитектуры](/D:/project/Self_core_java/docs/architecture/README.md)
- [Архитектура системы](/D:/project/Self_core_java/docs/architecture/system-architecture-ru.md)
- [Production-топология](/D:/project/Self_core_java/docs/architecture/production-topology-ru.md)

### 2. Микросервисы
- [Каталог микросервисов](/D:/project/Self_core_java/docs/services/README.md)

### 3. Интеграции
- [Обзор интеграционного раздела](/D:/project/Self_core_java/docs/integration/README.md)

### 4. Развёртывание
- [Обзор раздела развёртывания](/D:/project/Self_core_java/docs/deployment/README.md)
- [Production-руководство по развёртыванию](/D:/project/Self_core_java/docs/deployment/production-deployment-guide-ru.md)

### 5. Статус реализации
- [Обзор раздела статуса](/D:/project/Self_core_java/docs/status/README.md)

### 6. Архитектурные решения
- [ADR 0001. Модульный монорепозиторий](/D:/project/Self_core_java/docs/adr/0001-phase-a-monorepo.md)

## Логика организации документации

- `architecture/` содержит целевую архитектуру, срезы и эволюцию платформы.
- `services/` содержит отдельные документы по каждому микросервису.
- `integration/` содержит правила и примеры интеграции с внешними системами.
- `deployment/` содержит инструкции по запуску и развёртыванию.
- `status/` содержит текущую оценку готовности и демо-статус.
- `adr/` содержит архитектурные решения и принятые компромиссы.

## Правила ведения документации

- Все новые документы пишутся на русском языке.
- Все Markdown-файлы сохраняются в UTF-8 без BOM.
- Для каждого нового крупного технического блока должен обновляться соответствующий индексный README.
- При появлении новой подсистемы сначала обновляется архитектурный обзор, затем сервисный каталог, затем прикладные гайды.
