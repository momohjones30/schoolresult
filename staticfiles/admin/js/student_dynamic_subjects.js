// (function($) {
//     $(document).ready(function() {
//         // When the grade field changes
//         $('#id_Grade').change(function() {
//             var gradeId = $(this).val();
//             if (gradeId) {
//                 // Send AJAX request to fetch subjects
//                 $.ajax({
//                     url: '/admin/student/load-subjects/',
//                     data: {
//                         'grade_id': gradeId
//                     },
//                     success: function(data) {
//                         var subjectsSelect = $('#id_subjects');
//                         subjectsSelect.empty();  // Clear current subjects
//                         // Dynamically add checkboxes for subjects
//                         $.each(data, function(index, subject) {
//                             subjectsSelect.append(
//                                 '<input type="checkbox" name="subjects" value="' + subject.id + '"> ' + subject.name + '<br>'
//                             );
//                         });
//                     }
//                 });
//             } else {
//                 $('#id_subjects').empty();  // Clear if no grade is selected
//             }
//         });
//     });
// })(django.jQuery);
