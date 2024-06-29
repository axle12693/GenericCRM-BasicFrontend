$(document).ready(function() {
    $('#fetch-data').click(function() {
        $.ajax({
            url: 'https://jsonplaceholder.typicode.com/posts/1',
            type: 'GET',
            success: function(data) {
                $('#data-container').html(`
                    <h2>${data.title}</h2>
                    <p>${data.body}</p>
                `);
            },
            error: function() {
                $('#data-container').html('<p>An error has occurred</p>');
            }
        });
    });
});
