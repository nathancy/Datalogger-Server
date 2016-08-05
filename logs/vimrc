 set nocompatible
 filetype off

 set rtp+=~/.vim/bundle/Vundle.vim
 call vundle#begin()
 
 Plugin 'VundleVim/Vundle.vim'

 Plugin 'scrooloose/nerdtree'

 Plugin 'bling/vim-airline'

 Plugin 'Conque-Shell'

 Plugin 'kien/ctrlp.vim'

 Plugin 'easymotion/vim-easymotion'

 Plugin 'ervandew/supertab'

 Plugin 'sjl/gundo.vim'

 Plugin 'altercation/vim-colors-solarized'

 call vundle#end()
 filetype plugin indent on

 """"""""" NERDTree
 "Auto NERDtree when vim starts up
 " autocmd vimenter * NERDTree
 
 """""""""Set custom key to open NERDTree
 map <C-m> :NERDTreeToggle<CR> 

 """"""""" Airline (always show statusline)
 set laststatus=2

 """"""""" Conque Shell shortcut
 map <C-j> <C-w>j
 map <C-k> <C-w>k
 map <C-h> <C-w>h
 map <C-l> <C-w>l

 """""""" Conque shell magic resize
 :au WinEnter * :setlocal number
 :au WinEnter * :setlocal norelativenumber
 :au WinEnter * :wincmd =
 
 :au WinLeave * :setlocal nonumber
 :au WinLeave * :setlocal norelativenumber
 
 """"""""" CtrlP
 "let g:ctrlp_working_path_mode = 0
 "let g:ctrlp_map = '<c-p>'
 let g:ctrlp_cmd='CtrlP :pwd' 
 "noremap <C-a> :CtrlP ~/Spectrum/<CR>

 """"""""" EasyMotion
 "Disable default mapping
 let g:EasyMotion_do_mapping = 0
 
 """"""""" Jump to anywhere with one keybinding
 "s(char)enter(choose)
 nmap s <Plug>(easymotion-overwin-f)

 """"""""" Turn on case insensitive feature
 let g:EasyMotion_smartcase = 1

 """"""""" Line motions
 map <Leader>j <Plug>(easymotion-j)
 map <Leader>k <Plug>(easymotion-k)

 """"""""" Supertab
 let g:SuperTabDefaultCompletionType = "<c-n>"

 """""""""""""""
 "General settings
 """""""""""""""
 set autoindent
 set smartindent
 set tabstop=4
 set shiftwidth=4
 set expandtab
 set smarttab
 "set relativenumber
 """""""" Turns on line numbers 
 set number

 """""""" Toggle paste
 set pastetoggle=<F10>
 
 """""""" Copy paste in insert mode
 inoremap <C-v> <F10><C-r>+<F10>

 """""""" Opens new window on right and on bottom
 set splitright

 """""""" Minimum windows
 set winminwidth=10
 set winwidth=85
 set winheight=5
 set winminheight=5
 set winheight=45

 """""""" Allow mouse click to browse code
 "set mouse=a
 
 """""""" Set 7 lines to the cursor when moving vertically using j/k
 set so=7  
 
 """""""" Always show current position
 set ruler

 """""""" Set commandline space 
 "set cmdheight=1
 
 """""""" Ignore case when searching
 set ignorecase

 """""""" When searching try to be smart about cases
 set smartcase

 """""""" Highlight search results
 set hlsearch

 """""""" Incremental search
 set incsearch

 """""""" Show matching brackets when text indicator is over them
 set showmatch
 set matchtime=3
 
 """""""" HTML indenting
 filetype indent on
 let g:html_indent_inctags = "html, body, head, tbody"

 """""""" Set highlighting for other file types
 filetype on
 au BufNewFile, BufRead *.ino set filetype=c
 au BufNewFile, BufRead *.markdown, *.mdown, *.mkd, *.mkdn, *.md, setf markdown
 au BufNewFile, BufRead Gruntfile setf javascript

 """"""""""""""""""
 "Colors and Fonts
 """"""""""""""""""
 
 """""""" Syntax highlighting
 syntax enable 
 set background=dark
 "colorscheme default 
 """"""""""""""""""
 "Files, backup
 """"""""""""""""""
 set noswapfile

 """"""""""""""""""
 "Moving around, tabs
 """"""""""""""""""
 
 """""""" Return to last edit position when opening files
 autocmd BufReadPost *
    \ if line("'\"") > 0 && line("'\"") <= line("$") |
    \   exe "normal! g'\"" |
    \ endif

 """""""" Remember info about open files on close
 set viminfo^=%

 "let mapleader = ","
 "map <leader>cs :ConqueTermVSplit bash <cr>
 
