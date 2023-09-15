<?php
function get($url){
	$curl = curl_init();
	curl_setopt_array($curl, array(
	    CURLOPT_RETURNTRANSFER => 1,
	    CURLOPT_URL => $url,
	));

	$resp = curl_exec($curl);
	curl_close($curl);

	return $resp;
}

function save($data){
    $filename = 'backups/' . randstr(8) . '.html';
    $fp = fopen($filename, 'w');
    fwrite($fp, $data);
    fclose($fp);
    return $filename;
}

function randstr($length){
    $str = '';
    $chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    $size = strlen($chars);
    for ($i = 0; $i < $length; $i++) {
        $str .= $chars[rand(0, $size - 1)];
    }
    return $str;
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $url = $_POST["url"];
    $data = get($url);
    header('Location: ' . save($data));

} else {
    echo "Invalid request method";
}
?>
