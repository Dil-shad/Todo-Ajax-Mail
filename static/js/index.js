console.log("JS @@@");
$(document).ready(function () {
  fetchTodoData();
  //creating pagination buttons
  var contents = "";
  var links = $("#page-links");
  for (var i = 1; i <= 3; i++) {
    contents += `
      <a onclick="handlePaginationClick(${i})" class="btn page-link">${i}</a>
          `;
  }
  links.append(contents);
});

function fetchTodoData(pageNumber = 1, pageSize = 4) {
  let selected_filter = $("#filter").val();
  //var pageSize= document.getElementById("PageSizeInput");
  let search_term = $("#search").val();

  $.ajax({
    url: "/todo-list",
    data: {
      page: pageNumber,
      page_size: pageSize,
      filter: selected_filter,
      search: search_term,
    },
    dataType: "json",
    success: function (data) {
      console.log(data);
      generatePaginationLinks(data);
      var tbody = $("#tbody");
      var Content = "";

      for (let i = 0; i < data.todo.length; i++) {
        //const date=data.todo[i].date;
        //console.log(date);
        let task = data.todo[i];
        Content += generateTableRow(task);
      }

      tbody.html(Content);

      $("#showing-start").text(data.showing_start);
      $("#showing-end").text(data.showing_end);
      $("#total-count").text(data.count);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });
}

function generateTableRow(task) {
  return `
        <tr>
            <td>${task.title}</td>
            <td>${task.date}</td>
            <td>${task.repeat}</td>
            <td>${task.description}</td>
            <td><button class="btn btn-primary btn-sm"><a href="/task-update/${task.id}/"
            class="text-decoration-none text-white">EDIT</a></button>
            <button class="btn btn-danger btn-sm" type="button" onclick="DeleteTodoTask('${task.id}')" data-sid="">Delete</button>


</td>
        </tr>
    `;
}

//PAGINATION NEXT/PREVIOUS BTNS
function generatePaginationLinks(data) {
  var PageSizeInput = document.getElementById("PageSizeInput");
  var previous = document.getElementById("previous-page");
  var next = document.getElementById("next-page");

  if (data.previous_page_number !== null) {
    previous.style.display = "block";
    previous.onclick = function () {
      fetchTodoData(data.previous_page_number);
    };
  } else {
    previous.style.display = "none";
  }
  if (data.has_next !== false) {
    next.style.display = "block";
    next.onclick = function () {
      fetchTodoData(data.next_page_number);
      //console.log(data.next_page_number);
    };
  } else {
    next.style.display = "none";
  }
}

// PAGINATION BUTTONS (1,2,3)
function handlePaginationClick(pageNumber) {
  fetchTodoData(pageNumber);
}

// FOR SEARCH DROPDOWN
$(function () {
  $("#search").autocomplete({
    source: "/search-autocompletion",
    minLength: 2,
  });
});

//DELETE TASK
function DeleteTodoTask(pk) {
  console.log(pk);
  $.ajax({
    url: "/task-delete/" + pk + "/",
    data: "",
    dataType: "json",
    success: function (response) {
      console.log(response);
      fetchTodoData();
    },
  });
}

// SEND MAIL

function SendMail() {
  var address = $("#user_mail").val();
  var notify = $("#email-notification");
  var spinner = $("#loading-spinner");
  //spinner.show();
  spinner.html(`<span
   class="spinner-grow spinner-grow-sm"></span>
Sending`);
  $.ajax({
    type: "POST",
    url: "/send-email",
    data: { email: address },
    dataType: "json",
    success: function (response) {
      notify.show();
      if (response.status === "success") {
        console.log("Successfully sent: " + response.message);
        // Set a success alert

        notify.html(
          `<div class="alert alert-success alert-dismissible fade show">
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            <strong>Successfully!</strong> ${response.message}.
          </div>`
        );
      } else {
        console.log("Sending failed: " + response.message);
        // Set an error alert
        notify.html(
          `<div class="alert alert-danger alert-dismissible fade show">
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            <strong>Failed!</strong> ${response.message}.
          </div>`
        );
      }
    },
    error: function (xhr, status, error) {
      console.error(xhr, status, error);
    },
    complete: function () {
      //spinner.hide();
      spinner.html("Send");
    },
  });
}
