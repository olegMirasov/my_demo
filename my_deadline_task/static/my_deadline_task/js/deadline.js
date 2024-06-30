function moveTask() {
   let task_id = document.getElementById("myButton").value;
   BX24.callMethod("tasks.task.get", {'taskId': task_id, 'fields': ["DEADLINE"]}, function (res){
       let deadline = dayjs(res.answer.result.task['deadline']).add(1, 'day').format('DD.MM.YYYY HH:mm');
       BX24.callMethod("tasks.task.update", {'taskId': task_id, 'fields': {"DEADLINE": deadline.toString()}});
   })
   let info = document.getElementById("info").innerText = "Передвинуто с помощью JS";
}