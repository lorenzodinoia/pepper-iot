var robot;

QiSession(function (session) {
    console.log("connected!");
    robot = session;
    }, 
    function () {
    console.log("disconnected");
});

function start() {
    robot.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("PepperIoT/StartRoutine", []);
    });
}
/*
function test() {
    robot.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("PepperIoT/Requests/GetWards", []);
    });
}*/

function exit() {
    close();
}