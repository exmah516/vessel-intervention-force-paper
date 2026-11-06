% ---------------------------------
% 作者: latexstudio
% 网址: www.latexstudio.net
% 时间: 2023-04-27 19:31:56
% 描述: 《机器人》LaTeX模板
% 邮箱: latexstudio@qq.com
% ---------------------------------

\NeedsTeXFormat{LaTeX2e}[1999/12/01]
\ProvidesClass{JQRnew}[2023/04/27, v1.0 by latexstudio.net]

\LoadClass[twoside,twocolumn,a4paper,zihao={5}]{ctexart}

\RequirePackage{geometry}

\geometry{
  hmargin = {18.5mm,18.5mm},
  vmargin = {20mm,20mm},
  headsep = 3mm,
  includehead
}

\typeout{JQR template}

\def\normalsize{\fontsize{10.5bp}{14pt}\selectfont }

\RequirePackage[framemethod=TikZ]{mdframed}
\RequirePackage[numbers,sort&compress]{natbib}

\def\NAT@citexnum[#1][#2]#3{%
  \NAT@reset@parser
  \NAT@sort@cites{#3}%
  \NAT@reset@citea
  \@cite{\def\NAT@num{-1}\let\NAT@last@yr\relax\let\NAT@nm\@empty
    \@for\@citeb:=\NAT@cite@list\do
    {\@safe@activestrue
     \edef\@citeb{\expandafter\@firstofone\@citeb\@empty}%
     \@safe@activesfalse
     \@ifundefined{b@\@citeb\@extra@b@citeb}{%
       {\reset@font\bfseries?}
        \NAT@citeundefined\PackageWarning{natbib}%
       {Citation `\@citeb' on page \thepage \space undefined}}%
     {\let\NAT@last@num\NAT@num\let\NAT@last@nm\NAT@nm
      \NAT@parse{\@citeb}%
      \ifNAT@longnames\@ifundefined{bv@\@citeb\@extra@b@citeb}{%
        \let\NAT@name=\NAT@all@names
        \global\@namedef{bv@\@citeb\@extra@b@citeb}{}}{}%
      \fi
      \ifNAT@full\let\NAT@nm\NAT@all@names\else
        \let\NAT@nm\NAT@name\fi
      \ifNAT@swa
       \@ifnum{\NAT@ctype>\@ne}{%
        \@citea
        \NAT@hyper@{\@ifnum{\NAT@ctype=\tw@}{\NAT@test{\NAT@ctype}}{\NAT@alias}}%
       }{%
        \@ifnum{\NAT@cmprs>\z@}{%
         \NAT@ifcat@num\NAT@num
          {\let\NAT@nm=\NAT@num}%
          {\def\NAT@nm{-2}}%
         \NAT@ifcat@num\NAT@last@num
          {\@tempcnta=\NAT@last@num\relax}%
          {\@tempcnta\m@ne}%
         \@ifnum{\NAT@nm=\@tempcnta}{%
          \@ifnum{\NAT@merge>\@ne}{}{\NAT@last@yr@mbox}%
         }{%
           \advance\@tempcnta by\@ne
           \@ifnum{\NAT@nm=\@tempcnta}{%
             \ifx\NAT@last@yr\relax
               \def@NAT@last@yr{--\NAT@penalty}%
             \else
               \def@NAT@last@yr{--\NAT@penalty}%
             \fi
           }{%
             \NAT@last@yr@mbox
           }%
         }%
        }{%
         \@tempswatrue
         \@ifnum{\NAT@merge>\@ne}{\@ifnum{\NAT@last@num=\NAT@num\relax}{\@tempswafalse}{}}{}%
         \if@tempswa\NAT@citea@mbox\fi
        }%
       }%
       \NAT@def@citea
      \else
        \ifcase\NAT@ctype
          \ifx\NAT@last@nm\NAT@nm \NAT@yrsep\NAT@penalty\NAT@space\else
            \@citea \NAT@test{\@ne}\NAT@spacechar\NAT@mbox{\NAT@super@kern\NAT@@open}%
          \fi
          \if*#1*\else#1\NAT@spacechar\fi
          \NAT@mbox{\NAT@hyper@{{\citenumfont{\NAT@num}}}}%
          \NAT@def@citea@box
        \or
          \NAT@hyper@citea@space{\NAT@test{\NAT@ctype}}%
        \or
          \NAT@hyper@citea@space{\NAT@test{\NAT@ctype}}%
        \or
          \NAT@hyper@citea@space\NAT@alias
        \fi
      \fi
     }%
    }%
      \@ifnum{\NAT@cmprs>\z@}{\NAT@last@yr}{}%
      \ifNAT@swa\else
        \@ifnum{\NAT@ctype=\z@}{%
          \if*#2*\else\NAT@cmt#2\fi
        }{}%
        \NAT@mbox{\NAT@@close}%
      \fi
  }{#1}{#2}%
}%

\newcommand\ucite[1]{\textsuperscript{\:\cite{#1}}}

\RequirePackage{
  amsfonts      ,
  amsmath       ,
  amssymb       ,
  amsthm        ,
  array         ,
  balance       ,
  bicaption     ,
  % bm            ,
  booktabs      ,
  caption       ,
  diagbox       ,
  enumitem      ,
  etoolbox      ,
  fancyhdr      ,
  graphicx      ,
  indentfirst   ,
  layout        ,
  makecell      ,
  mathptmx      ,
  multirow      ,
  newtxtext     ,
  picinpar      ,
  qrcode        ,
  stfloats      ,
  tikz          ,
  tikzpagenodes ,
  titlesec      ,
  url           ,
  upgreek       ,
  xcolor        ,
  xeCJK         ,
  xparse        ,
}

\RequirePackage{bm}
\RequirePackage[small]{subfigure}

\graphicspath{{figs/}}
\urlstyle{same}
\xeCJKsetup{CheckSingle = true}

\ExplSyntaxOn
\sys_if_engine_xetex:TF{
  \PassOptionsToPackage{no-math}{fontspec}
}{}
\ExplSyntaxOff

\DeclareSymbolFont{myletters}{OML}{cmm}{m}{it}
\DeclareMathSymbol{\myepsilon}{\mathord}{myletters}{"0F}
\DeclareSymbolFont{oldsymbols}{OMS}{cmsy}{m}{n}
\DeclareSymbolFontAlphabet{\mathscr}{oldsymbols}
\DeclareSymbolFont{ugmL}{OMX}{mdugm}{m}{n}
\SetSymbolFont{ugmL}{bold}{OMX}{mdugm}{b}{n}
\DeclareMathAccent{\wideparen}{\mathord}{ugmL}{"F3}%
\DeclareSymbolFont{largesymbols}{OMX}{cmex}{m}{n}

\DeclareSymbolFont{EulerExtension}{U}{euex}{m}{n}
\DeclareMathSymbol{\euintop}{\mathop} {EulerExtension}{"52}
\let\intop\euintop
\let\ointop\euointop
\def\ge{\geqslant}
\def\geq{\geqslant}
\def\le{\leqslant}
\def\leq{\leqslant}
\newcolumntype{P}[1]{p{#1}<{\raggedright}}
\newcolumntype{R}[1]{p{#1}<{\raggedleft}}
\newcolumntype{C}[1]{p{#1}<{\centering}}

\usetikzlibrary{calc}
\captionsetup[figure][bi-second]{name=Fig.}
\captionsetup[table][bi-second]{name=Tab.}
\graphicspath{{./figs/},{./figures/}}

\DeclareCaptionFont{eightbp}{\fontsize{9bp}{9pt}\selectfont}

\captionsetup{
  labelsep        = quad,
  font            = eightbp,
  justification   = centering,
  singlelinecheck = false
}
\DeclareBiCaptionSeparator{-3pt}{\vspace{-4pt}}

\captionsetup[figure]{
  belowskip     = 2pt,
}
\captionsetup[table]{
  bi-separator  = -3pt,
  aboveskip     = 2pt,
  % belowskip     = 2pt,
}

% \AtBeginEnvironment{figure}{\intextsep 5pt plus 2pt minus 2pt \textfloatsep 5pt plus 2pt minus 2pt}
% \AtBeginEnvironment{figure*}{\intextsep 5pt plus 2pt minus 2pt \textfloatsep 5pt plus 2pt minus 2pt}
% \AtBeginEnvironment{table*}{\intextsep 10pt plus 2pt minus 2pt \textfloatsep 10pt plus 2pt minus 2pt}
% \AtBeginEnvironment{table}{\intextsep 10pt plus 2pt minus 2pt \textfloatsep 10pt plus 2pt minus 2pt}
\parskip 0pt
\columnsep 8mm
\intextsep 6pt plus 1pt minus 1pt
\textfloatsep 6pt plus 1pt minus 1pt
\floatsep 6pt plus 1pt minus 1pt
\partopsep 2pt plus 1pt minus 1pt
\lineskiplimit 2pt
\lineskip 2pt plus .1pt minus .1pt
\arraycolsep 4pt
\gdef\arraystretch{1.16}\selectfont
\gdef\baselinestretch{1.233}\selectfont
\footskip 250pt
\baselineskip=15.52bp plus 1pt minus 1pt%

\renewcommand\bibsection{%
 \vspace*{.4em}
 \section*{\refname\@mkboth{\MakeUppercase{\refname}}{\MakeUppercase{\refname}}}%
 \vskip 1.3ex
}%

\renewcommand{\labelenumi}{\arabic{enumi})}
\renewcommand{\labelenumii}{(\arabic{enumii})}

\def\lk{\linebreak}
\def\dd{{\rm d}}
\def\ee{{\rm e}}

\ExplSyntaxOn

\keys_define:nn { jqr } {
  % start~page . tl_set:N  = \l_jqr_startpage_tl,
  journal    . tl_set:N  = \l_jqr_journalcn_tl,
  journal    . initial:n = {机器人},
  journalen  . tl_set:N  = \l_jqr_journalen_tl,
  journalen  . initial:n = {ROBOT},
  volume     . tl_set:N  = \l_jqr_volume_tl,
  number     . tl_set:N  = \l_jqr_number_tl,
  year       . tl_set:N  = \l_jqr_year_tl,
  month      . tl_set:N  = \l_jqr_month_tl,
  doi        . tl_set:N  = \l_jqr_doi_tl,
  osid       . tl_set:N  = \l_jqr_osid_tl,
  year       . initial:n = 20xx,
  volume     . initial:n = xx,
  number     . initial:n = x,
  dox        . initial:n = xxxxxx,
  funds      . tl_set:N  = \l_jqr_funds_tl,
  cntitle    . tl_set:N  = \l_jqr_cntitle_tl,
  cnauthor   . tl_set:N  = \l_jqr_cnauthor_tl,
  runauthor  . tl_set:N  = \l_jqr_runauthor_tl,
  corrauthor . tl_set:N  = \l_jqr_corrauthor_tl,
  dates      . tl_set:N  = \l_jqr_dates_tl,
  runtitle   . tl_set:N  = \l_jqr_runtitle_tl,
  runtitle   . initial:n = {\l_jqr_runauthor_tl{}:~\l_jqr_title_tl},
  cnaddress  . tl_set:N  = \l_jqr_cnaddress_tl,
  cnabstract . tl_set:N  = \l_jqr_cnabstract_tl,
  cnkeywords . tl_set:N  = \l_jqr_cnkeywords_tl,
  CLC        . tl_set:N  = \l_jqr_CLC_tl,
  mark       . tl_set:N  = \l_jqr_mark_tl,
  mark       . initial:n = A,
  wzbh       . tl_set:N  = \l_jqr_wzbh_tl,
  wzbh       . initial:n = 0253-231X(20xx)05-xxxx-xx,
  entitle    . tl_set:N  = \l_jqr_entitle_tl,
  enauthor   . tl_set:N  = \l_jqr_enauthor_tl,
  enaddress  . tl_set:N  = \l_jqr_enaddress_tl,
  enabstract . tl_set:N  = \l_jqr_enabstract_tl,
  enkeywords . tl_set:N  = \l_jqr_enkeywords_tl
}

\NewDocumentCommand\JQRsetup{ +m }{
\keys_set:nn{jqr}{#1}
}

\NewDocumentCommand \l_jqr_enmonth_tl { }{
\int_case:nnF
  {\l_jqr_month_tl}
  {
    {1}  {Jan.}
    {2}  {Feb.}
    {3}  {Mar.}
    {4}  {Apr.}
    {5}  {May}
    {6}  {Jun.}
    {7}  {Jul.}
    {8}  {Aug.}
    {9}  {Sep.}
    {10} {Oct.}
    {11} {Nov.}
    {12} {Dec.}
  }
  {\color{red}No~ idea!}
}

\mdfdefinestyle{mystyle}{middlelinewidth=0,innerleftmargin=7.5mm,innerrightmargin=7.5mm}
\def\addr#1{\textsuperscript{#1}}

\coffin_new:N \l__rule_coffin
\coffin_new:N \l__ruleb_coffin
\coffin_new:N \l__journal_coffin
\coffin_new:N \l__doi_coffin
\coffin_new:N \l__cstr_coffin
\coffin_new:N \l__osid_coffin
\coffin_new:N \l__osidtext_coffin
\coffin_new:N \l__cninfo_coffin
\coffin_new:N \l__eninfo_coffin
\coffin_new:N \l__footnote_coffin

\def\JQRpubidadjcol{\enlargethispage{-\lenlargedim}}

\cs_new_nopar:Npn \l__coffin_ht_plus:N #1
  {
    \coffin_ht:N #1 + \coffin_dp:N #1
  }
\dim_new:N \lenlargedim
\cs_set_protected:Npn \__footnote_style:
{
  \vcoffin_set:Nnn \l__footnote_coffin {\linewidth}{
    \rule{33mm}{.4pt}\par \fontsize{8bp}{8pt}\selectfont
    \tl_if_empty:NF \l_jqr_funds_tl { 基金项目：\l_jqr_funds_tl．\par }
    通信作者：\l_jqr_corrauthor_tl \qquad 收稿\!／\!\!录用\!／\!\!修回： \l_jqr_dates_tl
  }
  \dim_gset:Nn \lenlargedim { \l__coffin_ht_plus:N \l__footnote_coffin + 10pt}
  \begin{tikzpicture}[remember~picture,overlay]
  \node[anchor~=~south~west,inner~sep=0pt,outer~sep=0pt,yshift=-1pt]~at~(current~page~text~area.south~west) {\coffin_typeset:Nnnnn \l__footnote_coffin {l}{t}{0pt}{0pt}};
  \end{tikzpicture}
}

\cs_set_protected:Npn \__title_style:
{
  \hcoffin_set:Nn \l__rule_coffin { \rule{\textwidth}{.2pt} }
  \hcoffin_set:Nn \l__ruleb_coffin { \rule{\textwidth}{.2pt} }
  \hcoffin_set:Nn \l__doi_coffin { \zihao{-5}\textbf{DOI}：10.13973/j.cnki.robot.\l_jqr_doi_tl \quad \textbf{CSTR}：32165.14.robot.\l_jqr_doi_tl}
  % \hcoffin_set:Nn \l__osidtext_coffin {\zihao{-5}\heiti  开放科学标识码（OSID）：}
  % \hcoffin_set:Nn \l__osid_coffin {\qrcode[height=13mm]{http://weixin.qq.com/q/\l_jqr_osid_tl}}
  \hcoffin_set:Nn \l__journal_coffin { \zihao{-4}\fangsong \l_jqr_journalcn_tl\kern 7mm \sffamily \l_jqr_journalen_tl }
  \hcoffin_set:Nn \l__cninfo_coffin {\zihao{-5} \makecell[l]{第~\l_jqr_volume_tl\ 卷第~\l_jqr_number_tl\ 期 \\[-3pt] \l_jqr_year_tl\ 年~\l_jqr_month_tl 月} }
  \hcoffin_set:Nn \l__eninfo_coffin { \zihao{-5} \makecell[r]{Vol.\l_jqr_volume_tl,\ No.\l_jqr_number_tl\\[-3pt] \l_jqr_enmonth_tl,\ \l_jqr_year_tl}}
  \coffin_join:NnnNnnnn
  \l__rule_coffin {l}{b}
  \l__ruleb_coffin {l}{t}
  {0pt}{-1.15pt}
  \coffin_join:NnnNnnnn
  \l__rule_coffin {\l__rule_coffin-l}{\l__rule_coffin-t}
  \l__cninfo_coffin {l}{b}
  {0pt}{-1.2pt}
  \coffin_join:NnnNnnnn
  \l__rule_coffin {\l__rule_coffin-hc}{\l__rule_coffin-t}
  \l__journal_coffin {hc}{b}
  {0pt}{5pt}
  \coffin_join:NnnNnnnn
  \l__rule_coffin {\l__rule_coffin-r}{\l__rule_coffin-t}
  \l__eninfo_coffin {r}{b}
  {0pt}{-1.2pt}
  \coffin_join:NnnNnnnn
  \l__rule_coffin {\l__ruleb_coffin-l}{\l__ruleb_coffin-b}
  \l__doi_coffin {l}{t}
  {0pt}{-6pt}
  % \tl_if_empty:NF \l_jqr_osid_tl
  % {
  %   \coffin_join:NnnNnnnn
  %   \l__rule_coffin {\l__ruleb_coffin-r}{\l__ruleb_coffin-b}
  %   \l__osid_coffin {r}{t}
  %   {0pt}{-6pt}
  %   \coffin_join:NnnNnnnn
  %   \l__rule_coffin {\l__osid_coffin-l}{\l__osid_coffin-t}
  %   \l__osidtext_coffin {r}{t}
  %   {-2pt}{0pt}
  % }
  \coffin_typeset:Nnnnn \l__rule_coffin {l}{t}{0pt}{0pt}
}

\AtBeginDocument{
  \renewcommand{\bibfont}{\fontsize{8.5pt}{8.5pt  plus .2pt minus .2pt} \selectfont }
  \bibsep 0pt
  \renewcommand\@biblabel[1]{[#1]\hfill}
  \fancypagestyle{main}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{.4pt}
  \fancyhead[EC]{\zihao{-5} \ziju{1}\l_jqr_journalcn_tl}
  \fancyhead[OC]{\zihao{-5} \l_jqr_runtitle_tl}
  \fancyhead[EL]{\zihao{-5} \l_jqr_year_tl\ 年~\l_jqr_month_tl 月}
  \fancyhead[OL]{\zihao{-5} 第~\l_jqr_volume_tl\ 卷第~\l_jqr_number_tl\ 期}
  \fancyhead[ER,OL]{\zihao{-5} \thepage}
  }
  \fancypagestyle{plain}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  }
  \pagestyle{main}
  \abovedisplayskip=5pt plus 0pt minus 1pt
  \belowdisplayskip=5pt plus 0pt minus 1pt
  \renewcommand{\@maketitle}{%
    \thispagestyle{plain}
    % \setcounter{page}{\l_jqr_startpage_tl}
    \label{FirstPage}
    \vspace*{-8mm}
    \__title_style:
    \vspace*{7mm}
    \begin{center}
    {\zihao{3}\bfseries\heiti\l_jqr_cntitle_tl\par}
    \vspace*{3mm}
    {\fangsong\zihao{4}\l_jqr_cnauthor_tl\par}
    \vskip 2pt
    {\zihao{6} （\l_jqr_cnaddress_tl）\par}
    \end{center}
    \parindent 2\ccwd
    \fontsize{9bp}{10pt}\selectfont
    \vspace*{-.8em}
    \begin{mdframed}[style=mystyle]
    \parindent 2em\par
    \begingroup
    \renewcommand\baselinestretch{1.3}\selectfont
    \hspace*{2em}{\heiti 摘\quad 要：}\l_jqr_cnabstract_tl\par
    \endgroup
    % \bigskip
    \hangindent 6em \hangafter 1
    {\heiti 关键词：} \l_jqr_cnkeywords_tl\par
    % {\heiti 中图分类号：}\makebox[3cm]{\l_jqr_CLC_tl\hfill }
    % {\heiti 文献标识码：}\makebox[3cm]{\l_jqr_mark_tl\hfill }
    % \tl_if_empty:NF \l_jqr_wzbh_tl
    % {
    %   {\heiti 文章编号：}\makebox[4cm]{\l_jqr_wzbh_tl\hfill }
    % }
    \end{mdframed}
    \begin{center}
    {\zihao{-4}\bfseries \l_jqr_entitle_tl\par}
    \vspace*{3mm}
    {\zihao{5} \l_jqr_enauthor_tl\par}
    % \medskip
    {\zihao{6} (\l_jqr_enaddress_tl)\par}
    \end{center}
    \fontsize{9pt}{10pt}\selectfont
    \vspace*{-.8em}
    \begin{mdframed}[style=mystyle]
    \parindent 1em
    \begingroup
    \renewcommand\baselinestretch{1.3}\selectfont
    \hspace*{1em}\textbf{Abstract:}~ \l_jqr_enabstract_tl\par
    \endgroup
    % \medskip
    \hangindent 6.1em \hangafter 1
    \textbf{Keywords:}~ \l_jqr_enkeywords_tl\par
    \end{mdframed}
    \__footnote_style:
    % \addtocounter{section}{-1}
    \vspace*{1pt plus.75pt minus.75pt}
  }
  \renewcommand\maketitle{\par
    \begingroup
      \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
      \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
      \long\def\@makefntext##1{\parindent 1em\noindent
              \hb@xt@1.8em{%
                  \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
      \if@twocolumn
        \ifnum \col@number=\@ne
          \@maketitle
        \else
          \twocolumn[\@maketitle]%
        \fi
      \else
        \newpage
        \global\@topnum\z@   % Prevents figures from going at top of page.
        \@maketitle
      \fi
      \thispagestyle{plain}\@thanks
    \endgroup
    \setcounter{footnote}{0}%
    \baselineskip=15.52bp plus 1pt minus 1pt%
    \JQRpubidadjcol
  }
}

\ExplSyntaxOff

\titleformat{name=\section}{\bfseries\heiti\zihao{-4}}{\thesection}{1em}{}

\def\refname{参考文献（References）}
\titleformat{name=\section,numberless}{\centering\bfseries\heiti\zihao{5}}{}{0em}{}

\titleformat{\subsection}{\bfseries\heiti\zihao{5} }{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\bfseries\heiti\zihao{5} }{\thesubsubsection}{1em}{}

\titlespacing{\section}{0pt}{1ex plus .5ex minus 1ex}{.3ex plus .1ex minus .1ex}
\titlespacing{\subsection}{0pt}{0pt}{.1ex minus .1ex}
\titlespacing{\subsubsection}{0pt}{0pt}{.1ex minus .1ex}

\AtBeginEnvironment{tabular}{\fontsize{9bp}{9.5bp}\selectfont }
\AtBeginEnvironment{tabular*}{\fontsize{9bp}{9.5bp}\selectfont }
\AtBeginEnvironment{tabularx}{\fontsize{9bp}{9.5bp}\selectfont }
\AtBeginEnvironment{thebibliography}{\fontsize{8bp}{8bp}\selectfont }



\def\th@definition{%
\normalfont            % body font
\thm@notefont{\normalfont }% same as heading font
\thm@preskip 2pt       % 定理类环境与正文文字的距离
\thm@postskip 2pt
\let\thm@indent\indent % no indent
}

\theoremstyle{definition}
\newtheorem{ example     }{ 例 }
\newtheorem{ definition  }{ 定义 }
\newtheorem{ theorem     }{ 定理 }
\newtheorem{ proposition }{ 性质 }
\newtheorem{ lemma       }{ 引理 }
\newtheorem{ corollary   }{ 推论 }
\newtheorem{ remark      }{ 注 }
\newtheorem{ step        }{ 步骤 }
\newtheorem{ hypothesis  }{ 步骤 }

\DeclareMathOperator{\diag}{diag}
\DeclareMathOperator{\rank}{rank}
\DeclareMathOperator{\tr}{tr}
\DeclareMathOperator{\sign}{sign}
\DeclareMathOperator{\sgn}{sgn}
\DeclareMathOperator{\Proj}{Proj}
\DeclareMathOperator{\argmin}{arg\,min}
\DeclareMathOperator{\argmax}{arg\,max}

\def\Intro #1（#2{%
 \hangafter 1\hangindent 4.5em\noindent\quad\zihao{-5}{\kaishu #1}\rm\songti（#2}
\def\enIntro #1 (#2{%
 \hangafter 1\hangindent 4.5em\noindent\quad\zihao{-5}{\bf #1}\rm~(#2}
 \newenvironment{enAuthorIntroduction}
{\vspace*{.8em}\noindent\bfseries\zihao{5}About Authors:\zihao{-5}\normalfont\par\vspace*{1mm}}
{}
 \newenvironment{AuthorIntroduction}
{\vspace*{.8em}\noindent\bfseries\heiti\zihao{5}作者简介：\zihao{-5}\normalfont\par\vspace*{1mm}}
  {}

\RequirePackage{hyperref}

\hypersetup{
  hidelinks,
  CJKbookmarks       = true,
  bookmarksnumbered  = true,
  bookmarksopen      = true,
  bookmarksopenlevel = 1,
  unicode            = true,
  colorlinks         = false,
  breaklinks         = false,
  backref            = false,
}

\AtEndDocument{\label{LastPage}}

\endinput

