window.onload = function() {
    var delete_button = document.getElementById("delete");
    var update_button = document.getElementById("update");
    var address = document.getElementById("address").getAttribute("href");
    var return_address = 'http://localhost:5000/favmovies';
    delete_button.onclick = function() {
        var request = new XMLHttpRequest();
        request.open('DELETE', address, false);
        request.send(null);
        if(request.status == 200) {
            console.log(request.responseText);
            window.alert(request.responseText);
            window.location = return_address;
        }
    }
    update_button.onclick = function() {
        var comment = document.getElementById("comment").value;
        var request = new XMLHttpRequest();
        request.open('PUT', address, false);
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        console.log(comment);
        request.send("comment="+comment);
        if(request.status == 200) {
            console.log(request.responseText);
            window.alert(request.responseText);
            window.location = return_address;
        }
    }
};
