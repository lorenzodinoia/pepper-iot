var robot;

QiSession(function (session) {
    console.log("connected!");
    robot = session;
    }, function () {
    console.log("disconnected");
});

function explore() {
    alert("Explore");
    robot.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("PepperIoT/StartExplore", []);
    });
}

function start() {
    robot.service("ALMemory").then(function (ALMemory) {
        ALMemory.raiseEvent("PepperIoT/StartRoutine", []);
    });
}

function exit() {
    close();
}
