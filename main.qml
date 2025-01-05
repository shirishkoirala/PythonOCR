import QtQuick
import QtQuick.Controls.Basic

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "HelloApp"
    Text {
        anchors.centerIn: parent
        text: "Hello World"
        font.pixelSize: 24
    }

    Button {
        text: "Select Folder"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20

         onClicked: {
            let folder = backend.select_folder();
            if (folder) {
                folder.text = "Selected: " + folder;
                console.log("Selected folder:", folder);
            } else {
                folder.text = "No folder selected";
            }
        }
    }
}