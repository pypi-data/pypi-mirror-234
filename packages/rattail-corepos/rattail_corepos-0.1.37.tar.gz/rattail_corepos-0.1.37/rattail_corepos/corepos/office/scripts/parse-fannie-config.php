<?php

$options = getopt('h', array(
    'help',
    'path:',
    'setting:',
));

$help = isset($options['h']) or isset($options['help']);
$path = isset($options['path']) ? $options['path'] : null;
$setting = isset($options['setting']) ? $options['setting'] : null;

if ($help or !$path or !$setting) {
    $script = basename($argv[0]);
    echo "Usage:  $script --path FANNIE_CONFIG_PATH --setting NAME_OF_SETTING\n";
    exit($help ? 0 : 1);
}

if (!is_file(realpath($path))) {
    echo "Config file does not exist: $path\n";
    exit(2);
}
$path = realpath($path);
include($path);

if (!isset($$setting)) {
    echo "Config file does not contain setting: $setting\n";
    exit(3);
}
$value = $$setting;

echo json_encode($value);

?>
