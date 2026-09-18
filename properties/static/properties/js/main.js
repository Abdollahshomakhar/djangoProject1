document.addEventListener('DOMContentLoaded', function () {
    var toggleBtn = document.getElementById('filterToggleBtn');
    var panel = document.getElementById('filterPanel');

    if (toggleBtn && panel) {
        toggleBtn.addEventListener('click', function () {
            var isOpen = panel.classList.toggle('is-open');
            toggleBtn.textContent = isOpen ? 'بستن فیلترها' : 'نمایش فیلترها';
        });
    }
});
