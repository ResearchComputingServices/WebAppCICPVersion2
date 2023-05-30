$(document).ready(function () {

    $(document).ready(function () {
        $('.select2').select2(); // Initialize Select2 on the select fields
    });

    $('.select-hidden').change(function () {
        var selectedOptions = $(this).val();
        var tagsContainer = $('#selected-options-tags');
        var selectedOptionsInput = $('#selected-options');

        tagsContainer.empty();

        if (selectedOptions.length > 0) {
            selectedOptionsInput.val(selectedOptions);

            for (var i = 0; i < selectedOptions.length; i++) {
                var optionValue = selectedOptions[i];
                var tag = $('<span class="tag">' + optionValue + '<a href="#" class="remove-tag" data-value="' + optionValue + '">&times;</a></span>');
                tagsContainer.append(tag);
            }
        } else {
            selectedOptionsInput.val('');
        }
    });

    $(document).on('click', '.remove-tag', function (e) {
        e.preventDefault();
        var tag = $(this).closest('.tag');
        var valueToRemove = $(this).data('value');
        var selectedOptionsInput = $('#selected-options');
        var selectedOptions = selectedOptionsInput.val().split(',');
        var index = selectedOptions.indexOf(valueToRemove);

        if (index !== -1) {
            selectedOptions.splice(index, 1);
            selectedOptionsInput.val(selectedOptions.join(','));
            tag.remove();
        }
    });


});

