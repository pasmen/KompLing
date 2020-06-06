#encoding "utf8"
#GRAMMAR_ROOT S

Attraction_FI -> Word<kwtype="Attractions">  Word<h-reg1, gram="од, имя, дат"> Word<h-reg1, gram="фам"> | Word<kwtype="Attractions"> Word<h-reg1, gram="фам, род, од"> | Word<kwtype="Attractions"> Word<kwtype="Author">;

Attraction -> Word<kwtype="Attractions"> Word<h-reg1, gram="прич, мн, род"> Word<h-reg1, gram="неод, мн, род"> | Word<kwtype="Attraction">;

S -> Attraction_FI interp(AttractionFIO.Name);

S -> Attraction interp(AttractionS.Name);


