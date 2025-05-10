// // Handle record deletion functionality
export function initRecordList() {
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const recordId = this.getAttribute('data-record-id');
            const csrfToken = document.querySelector('table').dataset.csrfToken;
            
            if (confirm('Are you sure you want to delete this record?')) {
                try {
                    const response = await fetch(`/delete/${recordId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    if (response.ok) {
                        this.closest('tr').remove();
                    } else {
                        throw new Error('Failed to delete record');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Error deleting record: ' + error.message);
                }
            }
        });
    });
}
// export function initRecordList() {
//     document.addEventListener('DOMContentLoaded', function() {
//     // Handle delete button clicks
//     document.querySelectorAll('.delete-btn').forEach(btn => {
//         btn.addEventListener('click', async function(e) {
//             e.preventDefault();
//             const recordId = this.getAttribute('data-record-id');
            
//             if (confirm('Are you sure you want to delete this record?')) {
//                 try {
//                     const response = await fetch(`/delete/${recordId}/`, {
//                         method: 'POST',
//                         headers: {
//                             'X-CSRFToken': '{{ csrf_token }}',
//                             'Content-Type': 'application/json'
//                         }
//                     });
                    
//                     if (response.ok) {
//                         // Remove the row from table without reloading
//                         this.closest('tr').remove();
//                     } else {
//                         throw new Error('Failed to delete record');
//                     }
//                 } catch (error) {
//                     console.error('Error:', error);
//                     alert('Error deleting record: ' + error.message);
//                 }
//             }
//         });
//     });
// });
// }