s.boot;
(
SynthDef(\simple_osc, {
	arg midinote = 60, vol = 0.1;
	var freq, sin, env;
	sin = SinOsc.ar(midinote.midicps, mul:vol);
	env = EnvGen.ar(Env.perc, doneAction:2);
	Out.ar(0, sin * env)
}).add;

OSCdef.new(\xylophone, {
	arg message, time, addr, port;
	message.do({ arg midinote, inx;
		if(inx > 0, {Synth(\simple_osc, [\midinote, midinote, \vol, 0.05]);});
	});
}, '/xylophone');

OSCdef.new(\bass, {
	arg message, time, addr, port;
	message.do({ arg midinote, inx;
		if(inx > 0, {Synth(\simple_osc, [\midinote, midinote, \vol, 0.1]);});
	});
}, '/bass');
)