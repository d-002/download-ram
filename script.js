let started, input, info, chunk, haha;

start = _=> {
	if (started) return;
	started = true;

	let value = parseInt(input.value.split(".")[0].replaceAll("-", ""));
	input.value = "-"+value;

	haha = [];
	info.innerHTMl = "Downloading RAM...";
	for (let i = 0; i < value; i++)
		haha.push(chunk+String.fromCharCode(Math.random()*1000));
	info.innerHTML = "Downloaded RAM: -"+value+"MB";
}

reset = _=> {
	if (started == false) return;
	started = false;

	haha = [];
	info.innerHTML = "Downloaded RAM: none";
}

init = _=> {
	let getId = i => document.getElementById(i), s = getId("start"), r = getId("reset");
	input = getId("input"), info = getId("info");
	chunk = ".";
	for (let i = 0; i < 1048575; i++) chunk += String.fromCharCode(Math.random()*1000);
	reset();
	s.addEventListener("click", start); r.addEventListener("click", reset);
}
