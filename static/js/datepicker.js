// $(document).ready($(function () {

//     var fridayDate = function () {
//         var curr;
//         curr = new Date();
//         var fridayDate
//         fridayDate = new Date();
//         var friday;
//         if (curr.getDay() == 0 || 1 || 2 || 3 || 4) {
//             friday = curr.getDay() + 2
//             fridayDate.setDate(fridayDate.getDate() - friday)
//             return fridayDate
//         }
//         else {
//             friday = curr.getDay() - 1
//             fridayDate.setDate(fridayDate.getDate() - friday)
//             return fridayDate
//         }

//     };


//     $(".dateinput").datepicker({
//         minDate: new Date("12/07/2022"),
//         maxDate: new Date(),
//         changeMonth: true,
//         changeYear: true,
//         showOn: 'button',
//         buttonText: 'Date',
//         dateFormat: 'yy-mm-dd',
//         defaultDate: fridayDate(),
//         beforeShowDay:
//             function (date) {
//                 return [
//                     date.getDay() == 0 ||
//                         date.getDay() == 1 ||
//                         date.getDay() == 2 ||
//                         date.getDay() == 3 ||
//                         date.getDay() == 4 ||
//                         date.getDay() == 6 ? false : true];
//             },
//     });
// })
// );

$(document).ready(function () {
    var fridayDate = function () {
        var curr = new Date();
        var fridayDate = new Date();
        var friday;
        if (curr.getDay() == 0 || curr.getDay() == 1 || curr.getDay() == 2 || curr.getDay() == 3 || curr.getDay() == 4) {
            friday = curr.getDay() + 2;
            fridayDate.setDate(fridayDate.getDate() - friday);
            return fridayDate;
        } else {
            friday = curr.getDay() - 1;
            fridayDate.setDate(fridayDate.getDate() - friday);
            return fridayDate;
        }
    };

    // Create a hidden input field to hold the selected date value (optional)
    const hiddenInput = $('<input>').attr({
        type: 'hidden',
        name: 'report_date', // Add the name attribute to match your form field
        value: $.datepicker.formatDate('yy-mm-dd', fridayDate())
    });

    // Append the hidden input field to the body (optional)
    $('body').append(hiddenInput);

    // Create the datepicker
    $("#datepicker").datepicker({
        minDate: new Date("12/07/2022"),
        maxDate: new Date(),
        changeMonth: true,
        changeYear: true,
        buttonText: 'Date',
        dateFormat: 'yy-mm-dd',
        defaultDate: fridayDate(),
        beforeShowDay: function (date) {
            return [
                date.getDay() == 0 ||
                    date.getDay() == 1 ||
                    date.getDay() == 2 ||
                    date.getDay() == 3 ||
                    date.getDay() == 4 ||
                    date.getDay() == 6 ? false : true
            ];
        },
        onSelect: function (dateText) {
            hiddenInput.val(dateText);
            // If you want to submit the form automatically when a date is selected
            // Uncomment the line below
            // $("form").submit();
        },
    });
});
