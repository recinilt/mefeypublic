"use strict"

/*
	(C) 2019, 2021 Christian Gottschall - all rights reserved
*/


class Wahrheitstabelle {

	constructor( exprs, html_id ) {
		this.exprs = exprs;

		this.constants = exprs[0].constants;
		
		for( let i = 1; i < exprs.length; i++ ) {
			this.constants = this.constants.concat( exprs[i].constants );
		}
		this.constants = this.constants.sort().filter(
					function( i, p, a ) { return p == 0 || i != a[p-1] }
				 );
		this.var_cnt = this.constants.length;

		this.val = (1 << this.var_cnt) - 1;
		this.html_id = html_id;
		this.tab = document.createElement("table");
	}

	dom_obj() {
		return this.tab;
	}

	html_table( detail ) {
		let	container = document.getElementById( this.html_id ),
			tab = this.tab,
			tb = document.createElement("tbody"),
			th = document.createElement("thead");

		tab.className = detail ? "Detailtabelle" : "Uebersichtstabelle";

		tab.style.width = "auto";

		for ( let i = container.children.length-1; i >= 0; i-- )
			container.children[i].remove();

		let r = document.createElement("tr"), c = null, t;

		tb.style.zIndex = 5;

		for ( let j = 0; j < this.var_cnt; j++ ) {
			c = document.createElement("th");
			t = document.createTextNode( this.constants[j] );
			c.appendChild(t);
			r.appendChild(c);

		}
		if ( c )
			c.style.paddingRight = "1em";

		for ( let j = 0; j < this.exprs.length; j++ ) {
			if ( detail ) {
				this.exprs[j].toHtml( r );
			} else {
				c = document.createElement("th");
				c.style.textAlign = "center";
				c.style.paddingLeft = "0.5em";
				c.style.paddingRight = "0.5em";
				t = document.createTextNode( this.exprs[j].toString() );
				c.appendChild(t);
				r.append(c);
			}
		}

		th.appendChild(r);
		tab.appendChild(th);

		for ( let i = this.val; i >= 0; i-- ) {
			r = document.createElement("tr");

			for ( let j = 0; j < this.var_cnt; j++ ) {
				c = document.createElement("td");
				t = document.createTextNode(
					(i & (1 << (this.var_cnt - j - 1))) ? "T" : "F"
				    );
				c.appendChild(t);
				r.appendChild(c);
			}
			c.style.paddingRight = "1em";

			for ( let j = 0; j < this.exprs.length; j++ ) {
				if ( detail ) {
					this.exprs[j].evaluate_to_html( i, this.constants, r, 0 );
				} else {

					c = document.createElement("td");
					c.style.textAlign = "center";
					t = document.createTextNode(
						this.exprs[j].evaluate( i, this.constants ) ?  "T" : "F"
					);
					c.appendChild(t);
					r.appendChild(c);
				}
			}

			tb.appendChild(r);
		}

		tab.appendChild(tb);

		container.appendChild(tab);

		container.scrollIntoView(true);
	}

}


