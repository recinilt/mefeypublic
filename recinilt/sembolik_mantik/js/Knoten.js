"use strict"

/*
	(C) 2019 Christian Gottschall - all rights reserved
*/


class Knoten {

	constructor( name, arity, eval_fun, constants ) {
		this.name = name;
		this.arity = arity;
		this.children = [];
		this.eval_fun = eval_fun;
		this.constants = constants;
	}

	get_child( i ) {
		return this.children[i];
	}

	set_child( i, c ) {
		this.children[i] = c;
	}

	evaluate( v, constants ) {
		if ( constants == null )
			constants = this.constants;
		if ( this.arity == 2 ) {
			return this.eval_fun(
				this.children[0].evaluate(v,constants),
				this.children[1].evaluate(v,constants)
			);
		} else if ( this.arity == 1 ) {
			return this.eval_fun(
				this.children[0].evaluate(v,constants)
			);
		} else if ( this.arity == 0 ) {
			let	i = constants.indexOf( this.name ),
			 	m = 1 << (constants.length - i - 1),
				r = (v & m) ? true : false;
			return	r;
		} else {
			alert( "Internal error, arity is " + this.arity + 
			       " on evaluation" );
			return false;
		}
	}


	evaluate_to_html( v, constants, tr, depth ) {
		if ( constants == null )
			constants = this.constants;

		if ( depth == null )
			depth = 0;

		let cell, text;

		if ( this.arity == 2 ) {
			let r = this.evaluate( v, constants );

			cell = document.createElement("td");
			text = document.createTextNode( "" );
			cell.appendChild( text );
			tr.appendChild( cell );

			this.children[0].evaluate_to_html(v, constants, tr, depth + 1 );
				
			cell = document.createElement( "td" );
			if ( depth == 0 ) {
				cell.style.fontSize = "125%";
				cell.style.fontWeight = "bold";
				cell.style.zIndex = "5";
			}
			text = document.createTextNode( r ? "T" : "F" );
			cell.appendChild( text );
			tr.appendChild( cell );

			this.children[1].evaluate_to_html(v, constants, tr, depth + 1 );

			cell = document.createElement("td");
			text = document.createTextNode( "" );
			cell.appendChild( text );
			tr.appendChild( cell );

			return r;
		} else if ( this.arity == 1 ) {
			let r = this.evaluate( v, constants );

			cell = document.createElement( depth ? "td" : "th" );
			if ( depth == 0 ) {
				cell.style.fontSize = "125%";
			}
			text = document.createTextNode( r ? "T" : "F" );
			cell.appendChild( text );

			tr.append( cell );

			this.children[0].evaluate_to_html( v, constants, tr, depth + 1  );

			return r;
		} else if ( this.arity == 0 ) {
			let	i = constants.indexOf( this.name ),
			 	m = 1 << (constants.length - i - 1),
				r = (v & m) ? true : false;

			cell = document.createElement( depth ? "td" : "th" );
			text = document.createTextNode( depth == 0 ?
				(r ? "T" : "F") : "" );
			cell.appendChild( text );

			tr.append( cell );

			return	r;
		} else {
			alert( "Internal error, arity is " + this.arity + 
			       " on evaluation" );
			return false;
		}
	}


	toString() {
		if ( this.arity == 2 ) {
			return "(" + this.children[0].toString() + " " +
				this.name + " " +
				this.children[1].toString() + ")";
		} else if ( this.arity == 1 ) {
			return this.name + this.children[0].toString();
		} else if ( this.arity == 0 ) {
			return this.name;
		} else {
			alert( "Internal error, arity is " + this.arity + 
			       " in toString()" );
			return "";
		}
	}


	toHtml(tr, d) {
		let t, c;
		if ( d == null ) d = 0
		if ( this.arity == 0 ) {
			c = document.createElement("th");
			t = document.createTextNode( this.name );
			c.appendChild( t );
			tr.appendChild( c );
		} else if ( this.arity == 1 ) {
			c = document.createElement("th");
			t = document.createTextNode( this.name );
			c.appendChild( t );
			tr.appendChild( c );
			this.children[0].toHtml( tr, d+1 );
		} else if ( this.arity == 2 ) {
			
			c = document.createElement("th");
			t = document.createTextNode( "(" );
			c.appendChild( t );
			tr.appendChild( c );

			this.children[0].toHtml(tr, d+1);

			c = document.createElement("th");
			t = document.createTextNode( this.name );
			c.appendChild( t );
			tr.appendChild( c );

			this.children[1].toHtml(tr, d+1);

			c = document.createElement("th");
			if ( d == 0 ) {
				c.style.paddingRight = "0.5em";
			}
			t = document.createTextNode( ")" );
			c.appendChild( t );
			tr.appendChild( c );
		} else {
			alert( "Internal error, arity is " + this.arity + 
			       " in toHtml()" );
		}
	}

}

