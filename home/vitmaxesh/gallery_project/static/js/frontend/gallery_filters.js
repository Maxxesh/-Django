document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('filter-category');
    const sortSelect = document.getElementById('sort-select');

    function updateURL() {
        const selectedCategory = categorySelect.value;
        const selectedSort = sortSelect.value;

        let newURL = window.location.pathname;

        const params = [];
        if (selectedCategory) {
            params.push('category=' + selectedCategory);
        }
        if (selectedSort) {
            params.push('sort=' + selectedSort);
        }

        if (params.length > 0) {
            newURL += '?' + params.join('&');
        }

        window.location.href = newURL;
    }

    categorySelect.addEventListener('change', updateURL);
    sortSelect.addEventListener('change', updateURL);
});