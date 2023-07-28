\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{rep1}
          [2023/05/13 v1 Charity insights Canada project]

\newif\if@Helvetica
\DeclareOption{Helvetica}{\@Helveticatrue}
\newif\if@Opensans
\DeclareOption{Opensans}{\@Opensanstrue}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extbook}}
\ProcessOptions\relax

\LoadClass[twoside,french]{extbook}
\RequirePackage[english]{babel}

\RequirePackage[letterpaper,%paperwidth=338.7mm,paperheight=190.5mm,
top=30mm,bottom=20mm,left=30mm,right=25mm,%showframe,
%headsep=8mm,
footskip=9mm,%headheight=40pt,
marginparwidth=0in]{geometry}

%------------------
%FONTS
%-------------------

\if@Helvetica
\RequirePackage[scaled]{helvet}
\renewcommand\familydefault{\sfdefault}
\else\fi
\if@Opensans
\RequirePackage[default]{opensans}
\else\fi

\RequirePackage[T1]{fontenc}
\RequirePackage[italic]{mathastext}%
%
\RequirePackage[all]{nowidow}
\RequirePackage{float}
\RequirePackage{ifthen}
\RequirePackage{booktabs}
\RequirePackage[table]{xcolor}
\RequirePackage{csvsimple-l3}
\RequirePackage{tabularray}
\UseTblrLibrary{amsmath,booktabs,counter,diagbox,siunitx,varwidth}
\RequirePackage{subcaption}
\DeclareCaptionFont{ninept}{\small #1}
\DeclareCaptionLabelFormat{r-parens}{#2}
\captionsetup[figure]{labelfont={bf,ninept},labelsep=colon,
belowskip=2pt,aboveskip=9pt,
justification=centering,singlelinecheck=false,font={bf,ninept}}
\captionsetup[table]{skip=8pt,labelfont={bf,ninept},labelsep=colon,
justification=centering,singlelinecheck=false,font={bf,ninept}}
%%
\captionsetup[subfigure]{labelformat=r-parens, labelsep=colon,
labelfont=bf,
font={bf,footnotesize},justification=centering,belowskip=0pt,aboveskip=6pt}
\renewcommand{\thesubfigure}{\Alph{subfigure}}

\definecolor{tablel}{RGB}{0,0,0}
\definecolor{titlecol}{RGB}{120,200,216}
\definecolor{redheder}{RGB}{228,29,35}
\definecolor{chapcol}{RGB}{0,0,0}
\parindent=0pt
\parskip=4pt plus 2pt minus 2pt

\RequirePackage{graphicx}
\graphicspath{{./figures/}}
\RequirePackage{xurl}
\urlstyle{same}

\RequirePackage{siunitx}
\sisetup{group-digits=integer,
            table-align-text-pre=false,
            table-align-text-post=false,
input-symbols		= ( ) [ ] - + *,
        }
\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\fi}

\RequirePackage{enumitem}
\setlist[enumerate]{nosep,label=\arabic*.,itemsep=4pt,labelindent=!, leftmargin=*,
labelsep=3pt, before={\vspace{0\baselineskip}},align=left,after={\vspace{0.5\baselineskip}}}
\setlist[itemize,1]{nosep,itemsep=2pt,labelindent=!, leftmargin=*,%10mm,
before={\vspace{0.25\baselineskip}},after={\vspace{0.1\baselineskip}}}

\RequirePackage{tikzpagenodes}
\RequirePackage{tikz}
\usetikzlibrary{positioning,fit}
\usetikzlibrary{calc}

\RequirePackage{calc}
\RequirePackage{array}
\def\mylength{\textwidth-2\tabcolsep-1.25\arrayrulewidth}
\RequirePackage[explicit]{titlesec}%
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{0}

\titlespacing*{\chapter}{0pt}{10pt plus 6pt}{20pt plus 6pt minus 6pt}

\RequirePackage{multicol}

\titleformat{name=\chapter,numberless}{\thispagestyle{first}}{}{0pt}%
{%
\begin{tikzpicture}[remember picture,overlay]
%\draw[green](current page text area.north west)rectangle(current page text area.south);
%\node[anchor=north west,draw=red,rectangle,minimum width=0.5\textwidth,
%minimum height=\textheight](RR)at(current page text area.north west){};
\node[anchor=west,text width=\columnwidth,outer sep=0pt,inner sep=0pt,
font={\fontsize{30pt}{30}\selectfont},align=left](CH)
at ($(current page text area.north west)!0.45!(current page text area.south west)$){#1};
\draw[line width=1.5pt,black!30]([yshift=-2mm]$(current page text area.north west)!0.48!(current page text area.north east)$)--
([yshift=2mm]$(current page text area.south west)!0.48!(current page text area.south east)$);
\end{tikzpicture}}[]

\titlespacing*{name=\chapter,numberless}{0pt}{0.4\textheight}{0.4\textheight}


%\addto\captionsgerman{% Replace "english" with the language you use
 % \renewcommand{\contentsname}%
  %  {Contents}%
%}

\titleformat{\section}
  {\color{black!90}\fontsize{14pt}{17pt}\selectfont\bfseries}
  {\thesection}%
  {0em}
  {#1}
  [\vskip-10pt{\makebox[\linewidth][l]{\raisebox{-1pt}{\color{chapcol!90}\rule{0.1\textwidth}{4.0pt}}%
  \color{chapcol!30}\rule{0.9\textwidth}{2.0pt}}}]
\renewcommand\thesection{}

\titlespacing*{\section}
{0mm}{12pt plus 2pt minus 3pt}{6pt plus 1pt minus 1pt}[0pc]


\titleformat{\subsection}
  {\color{black!70}\fontsize{13pt}{15pt}\selectfont\bfseries}
  {\thesubsection.}%
  {0.5em}
  {#1}
  [\vskip-12pt{\makebox[\linewidth][l]{\color{black!20}\rule{\textwidth}{0.5pt}}}]

\titlespacing*{\subsection}
{0mm}{24pt plus 2pt minus 3pt}{0pt plus 0pt minus 0pt}[0pc]


\titleformat{\subsubsection}
  {\color{black!70}\fontsize{12pt}{14pt}\selectfont\bfseries}
  {\thesubsubsection.}%
  {0.5em}
  {#1}
  [\vskip-12pt{\makebox[\linewidth][l]{\color{black!20} \rule{\textwidth}{0.51pt}}}]

\titlespacing*{\subsubsection}
{0mm}{12pt plus 2pt minus 3pt}{0pt plus 0pt minus 0pt}[0pc]

\titleformat{\paragraph}
  {\color{black!70}\fontsize{11pt}{12pt}\selectfont\bfseries}
  {\theparagraph}%
  {0.5em}
  {#1}
  []

\titlespacing*{\paragraph}
{0mm}{12pt plus 2pt minus 3pt}{1pt plus 1pt minus 1pt}[0pc]

\renewcommand{\thesubsection}{\Roman{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}

%----------------------------------------------------------------------------------------
%	TITLE
%----------------------------------------------------------------------------------------
\newcommand{\titleFrench}[1]{\def\@titleFrench{#1}}
\newcommand{\SubTitleFrench}[1]{\def\@SubTitleFrench{#1}}
\newcommand{\SubTitle}[1]{\def\@SubTitle{#1}}
% ---------------------------------------------------------------------
\renewcommand{\maketitle}{%
		\thispagestyle{empty}
\begin{tikzpicture}[remember picture,overlay]
%%%
\node[anchor=north west,rectangle,
minimum width=10mm,minimum height=\paperheight,
fill=white](TR)at (current page.north west){};
%%figure
\path[fill=white] node[anchor=north west,inner sep=2mm, %fill=white,
append after command={[rounded corners=8pt]([yshift=0mm]LO.west)|-(LO.north east)},
append after command={[rounded corners=0pt](LO.north)-|(LO.east)},
    append after command={[rounded corners=0pt](LO.east)|-(LO.south)},
    append after command={[rounded corners=0pt]([xshift=0mm]LO.south east)-|([yshift=0mm]LO.west)}]
(LO) at ([yshift=0mm]current page header area.north west){\includegraphics[scale=0.6]{/webapp/WebAppCICPVersion2/Latex/figures/logo_v}};
\node[align=flush left,text width=115mm,
%
inner sep=0,
anchor=south west,font={\fontsize{17pt}{13}\selectfont}](T2)
at([xshift=5mm,yshift=5mm]LO.south east){ };
%
\node[align=flush left,text width=115mm,
anchor=west,font={\fontsize{17pt}{13}\selectfont},
above=10mm of T2,inner sep=0,
%right=of $(LO.north east)!0.6!(LO.south east)$
](T1){CHARITY INSIGHTS CANADA PROJECT};
%%
\node[text width=150mm,align=flush left,redheder,
anchor=north,font={\fontsize{30pt}{25}\selectfont},
right=2mm of $(TR.north east)!0.24!(TR.south east)$,inner sep=0,
](T3){Weekly Report | Rapport Hebdomadaire};
%%%%%%TITLE
\node[text width=150mm,inner sep=0pt,align=flush left,
anchor=north,font={\bfseries\fontsize{25pt}{37}\selectfont},
below =14mm of T3](TIT1){\@title};%\MakeUppercaseat
\node[text width=150mm,inner sep=0pt,align=flush left,black!70,
anchor=north,font={\bfseries\fontsize{25pt}{37}\selectfont},
below =8mm of TIT1](TIT2){\@titleFrench};
%%%%%%SUBTITLE
\node[text width=150mm,inner sep=0pt,align=flush left,
anchor=west,font={\fontsize{18pt}{22}\selectfont},
below =10mm of TIT2](STIT1){\@SubTitle};
\node[text width=150mm,inner sep=0pt,align=flush left,
anchor=west,font={\fontsize{18pt}{22}\selectfont},black!70,
below =3mm of STIT1](STIT2){\@SubTitleFrench};
%
%%%%%%
%MEMBERS
%%%%%
\node[%draw=red,%
inner sep=0pt,
font={\fontsize{12pt}{12}\selectfont},anchor=east,
align=left](t1)
at
($(current page text area.east)!0.50!(current page text area.south east)$)
{%
\csvreader[
tabularray={%hlines, vlines,
width=0.91\textwidth,
colspec={Q[0.75,t,l]Q[1,t,l]Q[0.6,t,l]},
rows = {abovesep=0.1pt,belowsep=0.1pt,font={\fontsize{8pt}{10}\selectfont\color{black!70}}},
row{1,4,7,10,13,16}={abovesep=0.5pt,belowsep=0.5pt,font={\fontsize{8pt}{10}\selectfont\bfseries}},
  },
no head,late after line=\\,late after last line=\\,
    ]%
{/webapp/WebAppCICPVersion2/Latex/figures/members.txt}{}%
{\csvcoli & \csvcolii& \csvcoliii}
};
%%%
\node[anchor=south,inner sep=0mm, fill=white]%,below=10mm of t1]
(LO1)at([xshift=2mm]current page text area.south) {\includegraphics[scale=0.9]{/webapp/WebAppCICPVersion2/Latex/figures/logos}};
%
\node[anchor=north west,inner sep=8mm, below=5mm of LO1,
text width=150mm,inner sep=0pt,align=left,%flush left,
font={\fontsize{8pt}{11}\selectfont}]
(T4) {Please cite as, citez comme: CICP-PCPOB. (2023).
\textit{CICP-PCPOB Weekly Report- Rapport Hebdomadaire} (No. 1.1.3).
Philanthropy and Nonprofit Leadership, Carleton University.
\href{https://carleton.ca/cicp-pcpob/homepage/research-data/}{https://carleton.ca/cicp-pcpob/homepage/research-data/}};
\end{tikzpicture}
}

\newcommand{\HederTxt}[1]{\def\@HederTxt{#1}}
\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancypagestyle{car}{%
\renewcommand{\headrulewidth}{0pt}
  \fancyhf{}%
\fancyhead{\begin{tikzpicture}[remember picture,overlay]%draw=red,
\node[anchor=north west,rectangle,
minimum width=\paperwidth,minimum height=21mm,
fill=redheder](HH)at (current page.north west){};
\node[anchor=north east,inner sep=1mm]
(LOG) at ([yshift=7mm]current page header area.north east){\includegraphics[scale=0.7]{/webapp/WebAppCICPVersion2/Latex/figures/logo}};
%
\path[green](HH.west)-|coordinate(HT)(current page text area.north west);
\node[anchor=west,white,font={\fontsize{13pt}{15}\selectfont\bfseries},
inner sep=0pt,align=left]
at(HT) {\@HederTxt};
\end{tikzpicture}}
%
\fancyfoot[E]{%
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=east,black!60,font={\fontsize{10pt}{10}\selectfont},inner xsep=0pt]
at([xshift=0mm]current page footer area.south east) {\@title~|~\@titleFrench};
\node[anchor=west,black!90,font={\fontsize{9pt}{9}\selectfont},inner xsep=0pt]
at([yshift=0mm]current page footer area.south west) {\thepage};
\end{tikzpicture}}
%
\fancyfoot[O]{%
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=east,black!90,font={\fontsize{10pt}{10}\selectfont},inner xsep=0pt]
at([xshift=0mm]current page footer area.south east) {\thepage};
\node[anchor=west,black!60,font={\fontsize{9pt}{9}\selectfont},inner xsep=0pt]
at([yshift=0mm]current page footer area.south west) {\@title~|~\@titleFrench};
\end{tikzpicture}}
}

\fancypagestyle{first}{%
\renewcommand{\headrulewidth}{0pt}
  \fancyhf{}%
\fancyhead{\begin{tikzpicture}[remember picture,overlay]%draw=red,
\node[anchor=north west,rectangle,
minimum width=\paperwidth,minimum height=3mm,
fill=redheder](HH)at (current page.north west){};
\end{tikzpicture}}
%
\fancyfoot[E]{%
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=east,black!60,font={\fontsize{10pt}{10}\selectfont},inner xsep=0pt]
at([xshift=0mm]current page footer area.south east) {\@title~|~\@titleFrench};
\node[anchor=west,black!90,font={\fontsize{9pt}{9}\selectfont},inner xsep=0pt]
at([yshift=0mm]current page footer area.south west) {\thepage};
\end{tikzpicture}}
%
\fancyfoot[O]{%
\begin{tikzpicture}[remember picture,overlay]
\node[anchor=east,black!90,font={\fontsize{10pt}{10}\selectfont},inner xsep=0pt]
at([xshift=0mm]current page footer area.south east) {\thepage};
\node[anchor=west,black!60,font={\fontsize{9pt}{9}\selectfont},inner xsep=0pt]
at([yshift=0mm]current page footer area.south west) {\@title~|~\@titleFrench};
\end{tikzpicture}}
}

\RequirePackage[colorlinks,allcolors=blue]{hyperref} %

\renewcommand{\thefigure}{\arabic{figure}}
\renewcommand{\thetable}{\arabic{table}}
\renewcommand{\theequation}{\arabic{equation}}

\RequirePackage[many]{tcolorbox}

\definecolor{boxback}{RGB}{0,0,0}
\newtcolorbox{box1}[2][]{%
enhanced,breakable,
detach title,frame hidden,
borderline west={3pt}{0pt}{boxback},
before upper={\parskip=6pt},
%before upper={\fontsize{10pt}{13}\selectfont},
attach boxed title to top left={yshift=-\tcboxedtitleheight,yshifttext=-5mm},
colupper=black,colback=boxback!05,
boxed title style={frame hidden,borderline west={3pt}{0pt}{boxback}},
colbacktitle=boxback!05,
coltitle=black,
fonttitle=\large\bfseries,%center title,
left=1mm,right=0mm,
top=0mm,bottom=0mm,boxsep=2mm,arc=0mm, boxrule=1.0pt,%
title=#2,
%title=\ifx\hfuzz#2\hfuzz\else:~~#2\fi,
#1 }


\RequirePackage{chngcntr}
\counterwithout{figure}{chapter}
\counterwithout{table}{chapter}
\counterwithout{footnote}{chapter}

%%footnote indent
\long\def\@makefntext#1{\parindent 1em\noindent
    \@textsuperscript{\normalfont\@thefnmark}#1}%

%%%%
%APPENDIX
%%%%%

\let\oldappendix\appendix %% save current definition of \appendix
\renewcommand\appendix{\setcounter{figure}{0}\setcounter{table}{0}%
\counterwithin{figure}{chapter}
\counterwithin{table}{chapter}
\oldappendix
\newcommand{\section@cntformat}{\thesection\quad}%\appendixname~
\renewcommand\thechapter{\Alph{chapter}}
\renewcommand\thefigure{\thechapter.\arabic{figure}}
}

\newcommand*{\hintfont}{}
\definecolor{color0}{rgb}{0,0,0}
\newcommand*{\hintstyle}[1]{{\hintfont\textcolor{color0}{#1}}}

\newcommand*{\question}[3][3.5ex]{\par\addvspace{#1}%
  \begin{tabular}{@{}>{\raggedright\arraybackslash}p{1\mylength}}%
 	  \bfseries#2~\textbar \\[0.25ex]
      \textit{\color{black!70}#3}%
  \end{tabular}%
  }

\endinput
%% End of file `rep1.cls'
