document.addEventListener('DOMContentLoaded', function () {
    const ulCategory = document.getElementById('category-list');

    if (!ulCategory) {
        console.error('Элемент #ulCategory не найден. Убедитесь, что ваш <ul> имеет id="ulCategory"');
        return;
    }

    async function updateCategoryOnServer(categoryId, newCategoryName) {
        const url = `/admin-panel/api/categories/${categoryId}/`;
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
        const url = `/admin-panel/api/categories/delete/${categoryId}/`;
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

    async function processSave(parentLi, inputField) {
        const displaySpan = parentLi.querySelector('.item-display');
        const categoryId = parentLi.dataset.itemId;
        const newCategoryName = inputField.value.trim();

        if (newCategoryName === displaySpan.textContent.trim()) {
            displaySpan.style.display = 'inline';
            inputField.style.display = 'none';
            return;
        }

        if (!newCategoryName) {
            alert('Назва категорії не може бути порожньою!');
            inputField.value = displaySpan.textContent;
            displaySpan.style.display = 'inline';
            inputField.style.display = 'none';
            return;
        }

        const updatedCategory = await updateCategoryOnServer(categoryId, newCategoryName);

        if (updatedCategory) {
            displaySpan.textContent = updatedCategory.name;
        } else {
            inputField.value = displaySpan.textContent;
        }

        displaySpan.style.display = 'inline';
        inputField.style.display = 'none';
    }

    const itemDisplaySpans = document.querySelectorAll('span.item-display');
    itemDisplaySpans.forEach(spanElement => {
        spanElement.addEventListener('click', (e) => {
            const parentLi = spanElement.closest('li.editable-item');
            if (!parentLi) return;

            const inputField = parentLi.querySelector('.item-input');

            spanElement.style.display = 'none';
            inputField.style.display = 'inline-block';
            inputField.value = spanElement.textContent;

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

    ulCategory.addEventListener('focusout', async function (e) {
        const inputField = e.target.closest('.item-input');
        const parentLi = inputField ? inputField.closest('li.editable-item') : null;

        if (inputField && parentLi && !parentLi.contains(e.relatedTarget)) {
            await processSave(parentLi, inputField);
        }
    }, true);

    ulCategory.addEventListener('keypress', async function (e) {
        if (e.key === 'Enter') {
            const inputField = e.target.closest('.item-input');
            if (inputField) {
                e.preventDefault();
                const parentLi = inputField.closest('li.editable-item');
                await processSave(parentLi, inputField);
            }
        }
    });

    function getCsrfToken() {
        const csrfElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfElement) {
            return csrfElement.value;
        }
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) {
            return csrfMeta.content;
        }
        return null;
    }
});