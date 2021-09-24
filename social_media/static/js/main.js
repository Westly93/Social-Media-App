function commentReplyToggle(parrent_id){
    const row = document.getElementById(parrent_id);
    if (row.classList.contains('d-none')){
        row.classList.remove('d-none');
    }else{
        row.classList.add('d-none');
    }

}

function showNotifications(){
    const container= document.getElementById('notification-container');
    if(container.classList.contains('d-none')){
        container.classList.remove('d-none');
    }else{
        container.classList.add('d-none');
    }
}