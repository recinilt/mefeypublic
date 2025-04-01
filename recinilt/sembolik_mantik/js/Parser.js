"use strict"

/*
	(C) 2019 Christian Gottschall - all rights reserved
*/


class Parser {

	constructor( str ) {
		this.str = str;
		this.p = 0,
		this.token = null,
		this.err_msg = null,
		this.valid_chars = "¬∧⊼∨⊽→↔↮()",
		this.valid_propositions = "ABCDEFGHIJKLMNOPQRSTUVXYZ";
		this.constants = [];
		this.emend_cnt = 1;
	}

	reset( str ) {
		this.str = str;
		this.p = 0;
		this.token = null;
		this.err_msg = null;
		this.constants = [];
		this.emend_cnt = 1;
	}

	adderror( msg ) {
		if ( this.err_msg == null )
			this.err_msg = "";
		else
			this.err_msg += " ";
		this.err_msg += msg;
		return msg;
	}

	emend() {
		let str;
		do {
		      str = "P" + this.emend_cnt++;
		} while ( this.constants.includes(str) );
		return str;
	}

	emend_proposition( depth ) {
		let	r = Math.floor( Math.random() * 3 ),
			s = "P";

		if ( depth == null )
			depth = 0;

		if ( depth >= 4 )
			r = 0;
		else if ( depth < 3 && r < 2 )
			r = Math.floor( Math.random() * 2 ) + 1;

		if ( r == 0 ) {
			r = Math.floor( Math.random() *
				this.valid_propositions.length );
			s = this.valid_propositions[r];
		} else if ( r == 1 ) {
			s = '¬' + this.emend_proposition( depth + 1 );
		} else  {
			r =  Math.floor( Math.random() * 7 );
			s = "(" + this.emend_proposition( depth + 1 ) +
			    "∧∨⊼⊽→↔↮"[r] +
			    this.emend_proposition( depth + 1 ) + ")";
		}
		return s;

	}

	geterror() {
		return this.err_msg;
	}

	gettoken() {
		if ( this.str == null || this.str.length == 0 ) {
			this.adderror( "Empty string." );
			this.token = null;
			return null;
		} else if ( this.p >= this.str.length ) {
			this.token = null;
			return null;
		}

		while ( this.str[this.p] == ' ' )
			this.p++;

		if ( this.p >= this.str.length ) {
			this.token = null;
			return null;
		}

		if ( this.valid_chars.indexOf(this.str[this.p]) >= 0 ) {
			this.token = this.str[this.p++];
			return this.token;
		} else if ( this.valid_propositions.indexOf(this.str[this.p].toUpperCase()) >= 0 ) {
			this.token = this.str[this.p++].toUpperCase();
			while ( this.p < this.str.length &&
				"0123456789".indexOf(this.str[this.p]) >= 0 ) {
				this.token = this.token + this.str[this.p++];
			}
			return this.token;
		} else if ( this.str[this.p] == '&' ) {
			this.token = "∧";
			this.p++;
			if ( this.p < this.str.length && this.str[this.p] == '&' )
				this.p++;
			return this.token;
		} else if ( this.str[this.p] == '|' ) {
			this.token = "∨";
			this.p++;
			if ( this.p < this.str.length && this.str[this.p] == '|' )
				this.p++;
			return this.token;
		} else if ( this.str[this.p] == '~' || this.str[this.p] == '!' ) {
			this.token = "¬";
			this.p++;
			return this.token;
		}
		else if ( (this.str[this.p] == '=' || this.str[this.p] == '-') &&
			  this.str.length > this.p+1 && this.str[this.p+1] == '>' ) {
			this.p += 2;
			this.token = "→";
			return this.token;
		}
		else if ( this.str[this.p] == '<' && this.str.length > this.p+2 &&
			  (this.str[this.p+1] == '=' || this.str[this.p+1] == '-') &&
			  this.str[this.p+2] == '>' ) {
			this.p += 3;
			this.token = "↔";
			return this.token;
		}
		else {
			this.token = null;
			this.adderror( "Invalid character at position " + (this.p+1) + "." );
			return null;
		}
		alert( this.adderror( "Internal error: impossible case" ) );
		this.token = null;
		return null;
	}

	translate() {
		if ( this.gettoken() != null ) {
			let expr = this.bikonditional();
			if ( expr ) {
				expr.constants = this.constants.sort();
				if ( this.token != null )
					this.adderror( "End of expression expected before \""
					  + this.token + "\" at position " +
					  (this.p+1) + "." );
			}
			return expr;
		} else {
			let str = this.emend_proposition(0);
			this.reset( str );
			this.adderror( "Empty input, but you seemed to have \"" + str + "\" in mind." );
			return this.translate();
		}
	}

	bikonditional() {
		let x = this.konditional(), y, z;
		while( this.token != null && this.token == "↔" ) {
			this.gettoken();
			y = this.konditional();
			z = new Knoten( "↔", 2, function(a,b)
				{ return a == b; } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	konditional() {
		let x = this.disjunktion(), y, z;
		while( this.token != null && this.token == "→" ) {
			this.gettoken();
			y = this.disjunktion();
			z = new Knoten( "→", 2, function(a,b)
				{ return !a || b; } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	disjunktion() {
		let x = this.nor(), y, z;
		while( this.token != null && this.token == "∨" ) {
			this.gettoken();
			y = this.nor();
			z = new Knoten( "∨", 2, function(a,b)
				{ return a || b; } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	nor() {
		let x = this.xor(), y, z;
		while( this.token != null && this.token == "⊽" ) {
			this.gettoken();
			y = this.xor();
			z = new Knoten( "⊽", 2, function(a,b)
				{ return !(a || b); } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	xor() {
		let x = this.konjunktion(), y, z;
		while( this.token != null && this.token == "↮" ) {
			this.gettoken();
			y = this.konjunktion();
			z = new Knoten( "↮", 2, function(a,b)
				{ return (a && !b) || (b && !a); } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	konjunktion() {
		let x = this.nand(), y, z;
		while( this.token != null && this.token == "∧" ) {
			this.gettoken();
			y = this.nand();
			z = new Knoten( "∧", 2, function(a,b)
				{ return a && b; } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	nand() {
		let x = this.negation(), y, z;
		while( this.token != null && this.token == "⊼" ) {
			this.gettoken();
			y = this.negation();
			z = new Knoten( "⊼", 2, function(a,b)
				{ return !(a && b); } );
			z.set_child( 0, x );
			z.set_child( 1, y );
			x = z;
		}
		return x;
	}

	negation() {
		if ( this.token == null ) {
			let s = this.emend();
			this.adderror( "Unexpected end of expression. Did you mean " +
				       s + "?" );
			if ( ! this.constants.includes( s ) )
				this.constants.push( s );
			return new Knoten( s, 0, null );
		}
		let y,z;
		if ( this.token == "¬" || this.token == "~" ) {
			this.gettoken();
			y = this.negation();
			z = new Knoten( "¬", 1, function(a)
				{ return !a; } );
			z.set_child( 0, y );
			return z;
		} else if ( this.token == '(' ) {
			this.gettoken();
			z = this.bikonditional();
			if ( this.token == ')' )
				this.gettoken();
			else
				this.adderror( "Closed bracket expected at position " + (this.p+1) + "." );
			return z;
		} else {
			let s = this.token.toUpperCase();
			if ( ! s.match(/[A-Z][0-9]*/) ) {
				let t = this.emend();
				this.adderror( "Invalid propositional letter \""
					  + s + "\" at position " +
					  (this.p+1) +
					  ". Did you mean " + t + "?" );
				s = t;
			}

			if ( ! this.constants.includes( s ) )
				this.constants.push( s );
			z = new Knoten( s, 0, null );
			this.gettoken();
			return z;
		}
		alert( "Internal error: Impossible case in negation" );
		return null;
	}

}

