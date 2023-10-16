const socket = io.connect("/status"); // Status of the tests.
socket.on("connect", () => {
    console.log("socker.on('connect'){... }")
    $("#status-connected").show(); // className = "badge rounded-pill bg-success"
    $("#status-connecting").hide(); // className = "badge rounded-pill bg-success"
    reconnect()
});
socket.on("disconnect", () => {
    $("#status-connected").hide(); // className = "badge rounded-pill bg-success"
    $("#status-connecting").show(); // className = "badge rounded-pill bg-success"

});

function _rerun_test_term(test){
    ui_set_state(test, 'running', {'stacktrace': 'Test is running'});
    terminals[test][0].reset();
    terminals[test][0].writeln('Dashboard> Rerunning test..');
}
function re_run_all_tests(){
    socket.emit("rerun_all", {});
    for(test in terminals){
        _rerun_test_term(test);
    }
}
function re_run_test(test){
    socket.emit("rerun", {'test': test});
    _rerun_test_term(test);
}
function tests_and_state(){
    /** This function update the token/test results. **/
}

function ui_set_token_state(){
    /** React to a change in the .token file state **/
}
td_classes = {'fail': 'table-danger',
                 'pass': 'table-success',
                 'running': 'table-warning',
}

 $("#token-blurb").hide();
socket.on("token_update", function(data){
    console.log('> Updating token from remote...');
    // console.log(data);

    $("#token-blurb").show();
     for(const e of $(".current_token_file")){
        e.innerHTML = data.token;
     }
     for(k in data.results){
//        console.log(k);
//        console.log(data.results[k]);
        state = data.results[k];
         $("#tbl-"+k+"-token").removeClass();
        $("#tbl-"+k+"-token").addClass(td_classes[state]);
        $("#tbl-"+k+"-token")[0].querySelector("span").innerHTML = state;
    }
});


var questions = {}

function ui_set_state(test_id, state, data){
    /** Set the state of the test in the UI. Does not fire any events to the server. **/
   state_emojis = {'fail': "bi bi-emoji-frown",
                   'pass': "bi bi-emoji-smile",
                   'running': 'spinner-border text-primary spinner-border-sm',
    }
    state_classes = {'fail': 'text-danger',
                     'pass': 'text-success',
                     'running': 'text-warning',
    }
    $("#tbl-"+test_id+"-title").removeClass();
    $("#tbl-"+test_id+"-title").addClass(td_classes[state]);
    $("#tbl-"+test_id+"-unit").removeClass();
    $("#tbl-"+test_id+"-unit").addClass(td_classes[state]);
    tbl = $("#tbl-"+test_id+"-unit")[0];
    if (tbl != null){
        tbl.querySelector("span").innerHTML = state;
    }
    for(const e of $("." + test_id + "-status")){
        var icon = e.querySelector("#" + test_id + "-icon")
        if (icon != null){
                icon.setAttribute("class", state_emojis[state]);
        }
        var icon = e.querySelector("#" + test_id + "-status")
        if (icon != null){
            nc = state_classes[state]
//            console.log("coverage files changeD?", data.coverage_files_changed);
            if(data.coverage_files_changed != null){
                nc = nc + " text-decoration-line-through";
            }
            icon.setAttribute("class", nc);
        }
    }
    if (state == 'pass'){
            $('#'+test_id+'-stacktrace').html('The test passed successfully!')
    }
    if(state == 'fail'){
        js = " <script> $('.traceback').on('load', function() { console.log('STUFF');  do_call_doc_ready();   } ); </script>";
        js = "";
        if ( !(test_id in questions) ){
            questions[test_id] = {'stacktrace': ''}
        }
        /** We are doing this to avoid adding the same event listener twice. If we do that, we will open/close the trace (if added an even number of times) **/
        if (questions[test_id]['stacktrace'] == data.stacktrace){
            // Do nothing.
        }
        else{
            questions[test_id]['stacktrace'] = data.stacktrace;
            $('#'+test_id+'-stacktrace').html(data.stacktrace+js).ready(
                function(){
                     $('.'+test_id +"-traceback").ready( function() {
//                        console.log('in 200ms, I will call: do_call_doc_ready("' + test_id+'")');
                        setTimeout(function(){
                            do_call_doc_ready(test_id)
                        }, 200);
                    });
               });
           }
    }
}
// const status = document.getElementById("status");
/**
      socket.of("/admin").on("state", function (data) {
        console.log("new output received from server:", data.output);
        term.write(data.output);
      });

      socket.on("update", function (data) {
        console.log("new output received from server:", data.output);
        term.write(data.output);
      });

    socket.on('test_update', function (data){
        console.log('test got some new stuff');
    });

      function fitToscreen() {
        //fit.fit();
        const dims = { cols: term.cols, rows: term.rows };
        console.log("sending new dimensions to server's pty", dims);
        socket.emit("resize", dims);
      }
      **/

        socket.on("testupdate", function(data){
            console.log('> ', data.id, "updating to state", data.state)

            ui_set_state(data.id, data.state, data);
            const targetNode = document.getElementById(''+data.id+'-stacktrace');
            const callback = (mutationList, observer) => {
              for (const mutation of mutationList) {
              }
            };
            if(data.run_id != terminals[data.id][2]['run_id']){
                terminals[data.id][0].reset();
//                terminals[data.id][0].writeln('Dashboard> New run, resetting terminal');
                terminals[data.id][2]['run_id'] = data.run_id;
                terminals[data.id][2]['last_chunk_id'] = -1;
            }
            if(data.stdout != null){
                for (const o of data.stdout){
                    if (o[0] > terminals[data.id][2]['last_chunk_id']){
                        terminals[data.id][0].write(o[1]);
                        terminals[data.id][2]['last_chunk_id'] = o[0]
                    }
                }
//                if(data.state == 'pass' || data.state == 'fail' || data.state == 'error'){
//                    terminals[data.id][0].writeln("Dashboard> Test execution completed.")
//                }

            }
            return "function called on client side."
       });

      function debounce(func, wait_ms) {
        let timeout;
        return function (...args) {
          const context = this;
          clearTimeout(timeout);
          timeout = setTimeout(() => func.apply(context, args), wait_ms);
        };
      }
$("#status-connected").hide();
function reconnect(){
    console.log("> Reconnected to server...");
    socket.emit("reconnected", {'hello': 'world', 'id': socket.id});
    $("#status-connected").show(); // className = "badge rounded-pill bg-success"
    $("#status-connecting").hide(); // className = "badge rounded-pill bg-success"
}
const wait_ms = 50;
   //   window.onresize = debounce(fitToscreen, wait_ms);
//reconnect();
//window.onload = debounce(reconnect, wait_ms);

/** This block of code is responsible for managing the terminals */
//console.log(terminals);

for (var key in terminals) {
      const term = new Terminal({
       rows: 22,
        cursorBlink: true,
        macOptionIsMeta: true,
         scrollback: 5000,
        disableStdin: true,
        convertEol: true,
      });
      const fit = new FitAddon.FitAddon();
      term.loadAddon(fit);

      term.open(document.getElementById(key));
      fit.fit();
        term.writeln("Welcome back! Press the blue 'rerun' button above to run the test anew.")
        terminals[key] = [term, fit, {'last_run_id': -1, 'last_chunk': 0}]; // Last item are the state details.
}

 function fitToscreen() {
        mpt = $("#main_page_tabs")[0]
        for(k in terminals){
            e = mpt.querySelector("#"+k + "-pane");
            if ( e.classList.contains("active") ){
//                console.log("Fitting the terminal given by ", k)
                terminals[k][1].fit();
            }
            }
      }
window.onresize = debounce(fitToscreen, wait_ms);

$('button[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    for(key in terminals){
       terminals[key][0].write(''); // This appears to refresh the terminal.
    }
});


/** THIS CODE STORES THE CURRENTLY SELECTED TAB AND SELECTS IT AGAIN ON PAGE REFRESH **/
/* https://stackoverflow.com/questions/18999501/how-can-i-keep-selected-bootstrap-tab-on-page-refresh

$('#myTab button').click(function(e) {
  e.preventDefault();
  console.log("clicked")
  $(this).tab('show');
});

// store the currently selected tab in the hash value
$('button[data-toggle="tab"]').on("shown.bs.tab", function(e) {
  var id = $(e.target).attr("data-bs-target").substr(1);
  console.log(id);
  window.location.hash = id;
});

// on load of the page: switch to the currently selected tab
var hash = window.location.hash;
$('#myTab button[data-bs-target="' + hash + '"]').tab('show');
*/