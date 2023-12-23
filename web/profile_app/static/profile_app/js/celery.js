$(function () {

});

$('#task').on('click', getRunTask)

function getRunTask() {
  $.ajax({
    url: `/api/v1/profile/task/`,
    type: "GET",
    success: function (data) {;
      getStatusTask(data.task_id)
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}

function getStatusTask(task_id) {
  $.ajax({
    url: `/api/v1/profile/task/status/${task_id}`,
    type: "GET",
    success: function (data) {;
      if (data.status === "STARTED") {
        setTimeout(getStatusTask, 1000, task_id)
      } else if (data.status === "SUCCESS") {
        $(".task").addClass("task--success task--visible")
        setTimeout(() => {
          $(".task").removeClass("task--success task--visible")
        }, 1000)
      }
    },
    error: function (data) {
      console.log('error', data)
    }
  })
}
