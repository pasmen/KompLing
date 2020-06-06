#encoding "utf8"
#GRAMMAR_ROOT S
Chief_Deputy -> Word<kwtype=Deputy> | Word<kwtype=ChiefName>;
S -> Chief_Deputy<gram="од, ед"> interp(Chief.Name);
F_Name -> Word<h-reg2, ~quoted, gram="фам"> | Word<h-reg1, ~quoted, gram="фам"> Word<~quoted, gram="фам">;
I_Name -> Word<h-reg2, ~quoted, gram="имя"> | Word<h-reg1, ~quoted, gram="имя"> Word<~quoted, gram="имя">;
O_Name -> Word<h-reg2, ~quoted, gram="отч"> | Word<h-reg1, ~quoted, gram="отч"> Word<~quoted, gram="отч">;
Fio_name -> F_Name I_Name O_Name;
FIO_People -> Fio_name | Word<kwtype=FullNameArticle, ~quoted>;
S -> FIO_People interp(SAO.Name);

