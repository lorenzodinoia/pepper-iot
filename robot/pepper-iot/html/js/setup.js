var robot;

QiSession(function (session) {
    robot = session;
    robot.service("ALMemory").then(function (memory) {
            memory.subscriber("Result/GetWards").then(function (subscriber) {
                subscriber.signal.connect(function (data) {
                    wards = JSON.parse(data);
                    fillWards(wards);
                });                
            });
        });
    getWards();
    }, 
    function () {
    console.log("disconnected");
});

function getWards() {
    robot.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("PepperIoT/Requests/GetWards", []);
    });
}

function fillWards(wards) {
    var select = document.getElementById("wards");
    var i = 0;
    for (i = 0; i < wards.length; i++) {
        var element = document.createElement("option");
        element.innerHTML = wards[i].name_room;
        element.value = wards[i].id;
        select.appendChild(element);
    }
}

function startExploration() {
    var wardId = document.getElementById("wards").value;
    if (wardId != undefined) {
        robot.service("ALMemory").then(function (ALMemory) {
            //document.getElementById("wards").style.display = "none";
            //document.getElementById("buttonExplore").style.display = "none";
            //document.getElementById("explore").innerHTML("Esplorazione in corso");
            ALMemory.raiseEvent("PepperIoT/StartExplore", []);
        });
    }
}