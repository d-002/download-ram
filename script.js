let started, input, info, haha;

start = _=> {
	if (started) reset();
	started = true;

	let value = parseInt(input.value.split(".")[0].replaceAll("-", ""));
	input.value = "-"+value;

	haha = [];
	info.innerHTMl = "Downloading RAM...";
	for (let i = 0; i < value; i++)
		haha.push(new Uint32Array(131072));
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
	reset();
	s.addEventListener("click", start); r.addEventListener("click", reset);

	window.setInterval(_ => {if (haha-1 == null);}, 100);
}
