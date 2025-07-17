
document.addEventListener('DOMContentLoaded', function () {
    const ulCategory = document.getElementById('category-list'); // Получаем родительский UL

    if (!ulCategory) {
        console.error('Элемент #ulCategory не найден. Убедитесь, что ваш <ul> имеет id="ulCategory"');
        return;
    }

    // --- Функция для отправки запроса на сервер ---
    async function updateCategoryOnServer(categoryId, newCategoryName) {
        const url = `/moderation/api/categories/${categoryId}/`;
        const method = 'PUT';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ name: newCategoryName })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Не вдалося оновити категорію.');
            }

            const updatedCategory = await response.json();
            console.log('Категорія успішно оновлена:', updatedCategory);
            return updatedCategory;
        } catch (error) {
            console.error('Помилка при оновленні категорії:', error);
            alert('Помилка: ' + error.message);
            return false;
        }
    }

    async function deleteCategoryOnServer(categoryId) {
        const url = `/moderation/api/categories/delete/${categoryId}/`;
        const method = 'DELETE';
        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ categoryId })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Не вдалося видалити категорію.');
            }
            else {
                const message = await response.json();
                return true
            }
        } catch (error) {
            console.error('Помилка при видаленні категорії:', error);
            alert('Помилка: ' + error.message);
            return false;
        }
    };



    // --- Вспомогательная функция для обработки сохранения ---
    async function processSave(parentLi, inputField) {
        const displaySpan = parentLi.querySelector('.item-display');
        const categoryId = parentLi.dataset.itemId;
        const newCategoryName = inputField.value.trim();

        // Если значение не изменилось, просто переключим обратно без запроса
        if (newCategoryName === displaySpan.textContent.trim()) {
            displaySpan.style.display = 'inline';
            inputField.style.display = 'none';
            return;
        }

        // Валидация на пустую строку
        if (!newCategoryName) {
            alert('Назва категорії не може бути порожньою!');
            inputField.value = displaySpan.textContent; // Восстанавливаем старое значение
            displaySpan.style.display = 'inline';
            inputField.style.display = 'none';
            return;
        }

        const updatedCategory = await updateCategoryOnServer(categoryId, newCategoryName);

        if (updatedCategory) {
            displaySpan.textContent = updatedCategory.name; // Обновляем текст в span
        } else {
            // В случае ошибки, вернуть старое значение, если нужно
            inputField.value = displaySpan.textContent;
        }

        // Всегда возвращаемся в режим отображения после попытки сохранения
        displaySpan.style.display = 'inline';
        inputField.style.display = 'none';
    }

    // --- Прикрепляем слушатель клика К КАЖДОМУ span.item-display ---
    const itemDisplaySpans = document.querySelectorAll('span.item-display');
    itemDisplaySpans.forEach(spanElement => {
        spanElement.addEventListener('click', (e) => {
            const parentLi = spanElement.closest('li.editable-item');
            if (!parentLi) return;

            const inputField = parentLi.querySelector('.item-input');

            // Переключаем элементы видимости
            spanElement.style.display = 'none'; // targetSpan - это уже spanElement
            inputField.style.display = 'inline-block';
            inputField.value = spanElement.textContent; // Убеждаемся, что значение input актуально

            // Устанавливаем фокус и переводим курсор в конец
            inputField.focus();
            inputField.setSelectionRange(inputField.value.length, inputField.value.length);
        });
    });

    const itemDisplayButtons = document.querySelectorAll('button.btn-danger');
    itemDisplayButtons.forEach(displaybutton => {
        displaybutton.addEventListener('click', async (e) => {
            e.preventDefault()
            if (e.target.tagName == 'BUTTON') {
                const parentLi = e.target.closest('li.editable-item');
                const categoryId = parentLi.dataset.itemId;
                const delete_result = await deleteCategoryOnServer(categoryId);
                if (delete_result == true) {
                    if (parentLi) {
                        parentLi.remove()
                    }
                }
            }
        });
    });
    // --- Обработчик для сохранения изменений (потеря фокуса или Enter) ---
    // Эти слушатели по-прежнему используют делегирование на UL,
    // так как они относятся к input, который динамически становится видимым/невидимым.
    ulCategory.addEventListener('focusout', async function (e) {
        const inputField = e.target.closest('.item-input');
        const parentLi = inputField ? inputField.closest('li.editable-item') : null;

        // Проверяем, что фокус ушел именно с нашего inputField
        // и что он не ушел на что-то внутри этого же li (чтобы избежать повторного срабатывания)
        if (inputField && parentLi && !parentLi.contains(e.relatedTarget)) {
            await processSave(parentLi, inputField);
        }
    }, true);

    ulCategory.addEventListener('keypress', async function (e) {
        if (e.key === 'Enter') {
            const inputField = e.target.closest('.item-input');
            if (inputField) {
                e.preventDefault(); // Предотвращаем стандартное поведение Enter (например, отправку формы)
                const parentLi = inputField.closest('li.editable-item');
                await processSave(parentLi, inputField);
            }
        }
    });

    function getCsrfToken() {
        // В Django это обычно:
        const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfElement) {
            return csrfElement.value;
        }
        // Для Flask или других фреймворков может быть в мета-теге:
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            return csrfMeta.content;
        }
        return null;
    }
});