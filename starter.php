<?php
$city = $_POST['city'];
$link = '';

switch($city) {
    case 'Москва':
        $link = 'https://www.avito.ru/moskva/nedvizhimost';
        break;
    case 'Тула':
        $link = 'https://www.avito.ru/tula/nedvizhimost';
        break;
    case 'Санкт-Петербург':
        $link = 'https://www.avito.ru/sankt-peterburg/nedvizhimost';
        break;
    default:
        echo "Выбранный город не поддерживается";
        exit;
}

$command = "C:\Users\HoPe\AppData\Local\Programs\Python\Python311\python.exe main.py " . $link;

$descriptorspec = array(
    0 => array("pipe", "r"),  // stdin
    1 => array("pipe", "w"),  // stdout
    2 => array("pipe", "w")   // stderr
);

$process = proc_open($command, $descriptorspec, $pipes);

if (is_resource($process)) {
    fclose($pipes[0]);

    $output = stream_get_contents($pipes[1]);
    fclose($pipes[1]);

    $error_output = stream_get_contents($pipes[2]);
    fclose($pipes[2]);

    $return_value = proc_close($process);

    if ($return_value == 0) {
        echo "Скрипт успешно выполнен.<br>";
        echo "Вывод: <br>" . $output;
    } else {
        echo "Не удалось выполнить скрипт. Код ошибки: $return_value<br>";
        echo "Ошибка: <br>" . $error_output;
    }
} else {
    echo "Не удалось запустить процесс.";
}
?>
