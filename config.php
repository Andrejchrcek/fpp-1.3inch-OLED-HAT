<?php
include_once "/opt/fpp/www/common.php";

$pluginName = "fpp-oled_remote";
$logFile = "/home/fpp/media/logs/" . $pluginName . ".log";
$helperScript = "/home/fpp/media/plugins/" . $pluginName . "/helper.sh";

// Callback funkcia na aplikovanie zmien po uložení
function SaveConfig($status) {
    global $helperScript, $logFile;
    exec("sudo " . $helperScript . " >> " . $logFile . " 2>&1");
}
?>

<div id="oled-remote-settings" class="settingsGroup">
    <legend>🔌 OLED Remote Control Settings</legend>

    <p><em>When checked, the remote control script will start automatically with FPP after a restart.</em></p>
    <?php PrintSettingCheckbox("Enable Plugin on Startup", "enabled", $restart = 0, $reboot = 0, "1", "0", $pluginName, $changeCallback = '', $saveCallback = "SaveConfig"); ?>

    <p><em>Displays the battery percentage on the OLED screen.</em></p>
    <?php PrintSettingCheckbox("Show Battery Status", "showBattery", $restart = 0, $reboot = 0, "1", "0", $pluginName, $changeCallback = '', $saveCallback = "SaveConfig"); ?>
</div>
