"use strict"

/*
	C.G. 15.4.2017
	C.G. 10.2.2019  Löschtaste, Tabellenbau
*/


var cgTranslatedPropositions = null;
let fehlerfeld;


function knopfGedrueckt( element ) {
	let	eingabefeld = document.getElementById( "TextAreaAusdruck" );
	if ( ! eingabefeld )
		return;
	if ( element ) {
		let	text = element.innerHTML,
			alt = eingabefeld.value,
			neu = null;

		if ( typeof eingabefeld.selectionStart == "number" &&
		     typeof eingabefeld.selectionEnd == "number") {

			let	pfx = null, sfx = null,
				start = eingabefeld.selectionStart,
				end = eingabefeld.selectionEnd;

			pfx = start > 0 ? alt.substring( 0, start ) : "";
			sfx = end < alt.length ? alt.substring( end ) : "";
			neu = pfx + text + sfx;

			eingabefeld.value = neu;
			eingabefeld.selectionStart = start + text.length;
			eingabefeld.selectionEnd = end + text.length;
		} else {
			neu = alt + text;
			eingabefeld.value = neu;
		}
	}
	eingabefeld.focus();
}


function eingabeWaehlen() {
	let eingabefeld = document.getElementById( "TextAreaAusdruck" );
	eingabefeld.setSelectionRange( 0, eingabefeld.value.length );
}


function ueberschreibknopfGedrueckt(x) {
	eingabeWaehlen();
	knopfGedrueckt(x);
}



function allesLoeschen() {
	let	eingabefeld = document.getElementById( "TextAreaAusdruck" );

	if ( eingabefeld ) {
		eingabefeld.value = "";
	}
}


function loeschtaste() {

	let	eingabefeld = document.getElementById( "TextAreaAusdruck" );

	if ( eingabefeld ) {

		let	alt = eingabefeld.value,
			neu = null, start = 0, end = 0;

		if ( typeof eingabefeld.selectionStart == "number" &&
		     typeof eingabefeld.selectionEnd == "number" &&
		     (start = eingabefeld.selectionStart) != 
		     (end = eingabefeld.selectionEnd) ) {

			let	pfx = null, sfx = null;

			pfx = start > 0 ? alt.substring( 0, start ) : "";
			sfx = end < alt.length ? alt.substring( end ) : "";
			neu = pfx + sfx;

			eingabefeld.value = neu;
		} else {
			let l = alt.length;

			if ( l == 0 ) {
				fehlerfeld = document.getElementById( "Fehlerfeld" );
				if ( fehlerfeld ) {

					fehlerfeld.innerText = "The input field is empty. There is nothing to eat for the purple monster. Once that you have entered text, the purple munster will happily eat it.";
					fehlerfeld.style.display = "block";
					fehlerfeld.scrollIntoView(true);
				}
			} else {
				if (l <= 1)
					neu = "";
				else
					neu = alt.substring( 0, l-1 );
				eingabefeld.value = neu;
			}
		}
		eingabefeld.focus();
	}
}



function knoepfeZeigen() {
   let   knoepfe = document.getElementById('knoepfe');

   if ( knoepfe )
      knoepfe.style.display = 'initial';
}


function change_verbosity() {
	let	d = document.getElementById( "Detailtabelle" ),
		u = document.getElementById( "Uebersichtstabelle" ),
		b = document.getElementById( "VerbosityButton" ),
		dv = d ? d.style.display != "none" : false,
		uv = u ? u.style.display != "none" : false,
		wt = null;

	if ( (dv && uv) || (!dv && !uv) ) {
		dv = false;
		uv = true;
	} else {
		dv = ! dv;
		uv = ! uv;
	}

	if ( dv && ( !d.firstElementChild ||
		     d.firstElementChild.nodeName.toLowerCase() != "table") ) {
		wt = new Wahrheitstabelle( cgTranslatedPropositions,
				           "Detailtabelle" );
		wt.html_table(true);
	}
	if ( uv && ( !u.firstElementChild ||
		     u.firstElementChild.nodeName.toLowerCase() != "table") ) {
		wt = new Wahrheitstabelle( cgTranslatedPropositions,
				           "Uebersichtstabelle" );
		wt.html_table(false);
	}

	d.style.display = dv ? "block" : "none";
	u.style.display = uv ? "block" : "none";

	if ( b )
		b.textContent = (dv ? "Hide " : "Show ") +
				"intermediate results";

}


function tabellenbau() {
	let	eingabefeld = document.getElementById( "TextAreaAusdruck" ),
		fehlerfeld = document.getElementById( "Fehlerfeld" ),
		changeVerbosity = document.getElementById( "ChangeVerbosity" ),
		ueb = document.getElementById( "TruthTableHeader" ),
		wt = null;

	if ( ! eingabefeld ) {
		alert( "tabellenbau() kein Eingabefeld" );
		return null;
	}

	let	eingaben = eingabefeld.value.split(",");

	cgTranslatedPropositions = [];

	let	err = null;
	for ( let ei = 0; ei < eingaben.length; ei++ ) {
		let p = new Parser( eingaben[ei] );
		cgTranslatedPropositions.push( p.translate() );
		let akt_err = p.geterror();
		if ( akt_err ) {
			if ( err )
				err = err + "\n" + akt_err;
			else
				err = akt_err;
		}
	}

	let	d = document.getElementById( "Detailtabelle" ),
		u = document.getElementById( "Uebersichtstabelle" ),
		dv = d ? (d.style.display != "none") : false,
		uv = u ? (u.style.display != "none") : false;

	if ( (dv && uv) || (!dv && !uv) ) {
		dv = false;
		uv = true;
	}

	if ( cgTranslatedPropositions.length > 0 ) {

		let eneu = "";
		for ( let i = 0; i < cgTranslatedPropositions.length; i++ ) {
			if ( i ) eneu = eneu + ", ";
			eneu = eneu + cgTranslatedPropositions[i].toString();
		}
		eingabefeld.value = eneu;

		if ( dv ) {
			wt = new Wahrheitstabelle( cgTranslatedPropositions,
					      "Detailtabelle" );
			wt.html_table(true);
			while( u.firstChild )
				u.removeChild( u.firstChild );
		}
		if ( uv ) {
			wt = new Wahrheitstabelle( cgTranslatedPropositions,
					      "Uebersichtstabelle" );
			wt.html_table(false);
			while( d.firstChild )
				d.removeChild( d.firstChild );
		}


		if ( changeVerbosity ) {
			changeVerbosity.style.display = "block";
		}
	}

	if ( fehlerfeld ) {

		if ( err ) {
			fehlerfeld.innerText = err;
			fehlerfeld.style.display = "block";
			fehlerfeld.scrollIntoView(true);
		} else {
			fehlerfeld.innerText = "No errors so far.";
			fehlerfeld.style.display = "none";
		}
	}

	if ( ueb && ! err )
		ueb.scrollIntoView(true);
}


function wahrheitstabelle_script_enabled() {
	let	ta = document.getElementById("TextAreaAusdruck"),
		js = document.getElementById("scriptsEnabled");

	if ( ta ) {
		/*XXX
		let fn = function() {
			ta.readOnly = true;
			window.removeEventListener( "touchstart", fn );
		};
		window.addEventListener( "touchstart", fn ); XXX*/

		ta.addEventListener( 'keyup',
			function(e) {
				e.preventDefault();
				if ( e.keyCode === 13 )
					document.getElementById('AcceptButton').click();
			} );
	}

	if ( js ) {
		js.style.display = "inline";
	}


}

