



<!DOCTYPE html>
<html lang="en" class="   ">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    
    
    <title>ScrollToFixed/jquery-scrolltofixed-min.js at master · bigspotteddog/ScrollToFixed · GitHub</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="bigspotteddog/ScrollToFixed" name="twitter:title" /><meta content="ScrollToFixed - This plugin is used to fix elements on the page (top, bottom, anywhere); however, it still allows the element to continue to move left or right with the horizontal scroll." name="twitter:description" /><meta content="https://avatars3.githubusercontent.com/u/865101?v=2&amp;s=400" name="twitter:image:src" />
<meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars3.githubusercontent.com/u/865101?v=2&amp;s=400" property="og:image" /><meta content="bigspotteddog/ScrollToFixed" property="og:title" /><meta content="https://github.com/bigspotteddog/ScrollToFixed" property="og:url" /><meta content="ScrollToFixed - This plugin is used to fix elements on the page (top, bottom, anywhere); however, it still allows the element to continue to move left or right with the horizontal scroll." property="og:description" />

    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="conduit-xhr" href="https://ghconduit.com:25035">
    

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>
      <meta name="google-analytics" content="UA-3769691-2">

    <meta content="collector.githubapp.com" name="octolytics-host" /><meta content="collector-cdn.github.com" name="octolytics-script-host" /><meta content="github" name="octolytics-app-id" /><meta content="2A94A9CB:6A3E:AB39C9C:540821EA" name="octolytics-dimension-request_id" />
    

    
    
    <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">


    <meta content="authenticity_token" name="csrf-param" />
<meta content="juFEf7vB5lrK6aNzx+8Sg1l7g0cUE8XAr4R2DgeDEQ/4e/FNgNeyBZVYDI8HlX8Uyc6cAoHUOcQ//g+PQewCpw==" name="csrf-token" />

    <link href="https://assets-cdn.github.com/assets/github-c0c2293be58dbb87efbe15f0252a75aa7f738724.css" media="all" rel="stylesheet" type="text/css" />
    <link href="https://assets-cdn.github.com/assets/github2-2c7d4f87e135381585a949e74aa65d44cca0232f.css" media="all" rel="stylesheet" type="text/css" />
    


    <meta http-equiv="x-pjax-version" content="62537849d5f6d9949c1a651bcb33b773">

      
  <meta name="description" content="ScrollToFixed - This plugin is used to fix elements on the page (top, bottom, anywhere); however, it still allows the element to continue to move left or right with the horizontal scroll.">
  <meta name="go-import" content="github.com/bigspotteddog/ScrollToFixed git https://github.com/bigspotteddog/ScrollToFixed.git">

  <meta content="865101" name="octolytics-dimension-user_id" /><meta content="bigspotteddog" name="octolytics-dimension-user_login" /><meta content="1931236" name="octolytics-dimension-repository_id" /><meta content="bigspotteddog/ScrollToFixed" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="1931236" name="octolytics-dimension-repository_network_root_id" /><meta content="bigspotteddog/ScrollToFixed" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/bigspotteddog/ScrollToFixed/commits/master.atom" rel="alternate" title="Recent Commits to ScrollToFixed:master" type="application/atom+xml">

  </head>


  <body class="logged_out  env-production windows vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>
    <div class="wrapper">
      
      
      
      


      
      <div class="header header-logged-out">
  <div class="container clearfix">

    <a class="header-logo-wordmark" href="https://github.com/" ga-data-click="(Logged out) Header, go to homepage, icon:logo-wordmark">
      <span class="mega-octicon octicon-logo-github"></span>
    </a>

    <div class="header-actions">
        <a class="button primary" href="/join" data-ga-click="(Logged out) Header, clicked Sign up, text:sign-up">Sign up</a>
      <a class="button signin" href="/login?return_to=%2Fbigspotteddog%2FScrollToFixed%2Fblob%2Fmaster%2Fjquery-scrolltofixed-min.js" data-ga-click="(Logged out) Header, clicked Sign in, text:sign-in">Sign in</a>
    </div>

    <div class="site-search repo-scope js-site-search">
      <form accept-charset="UTF-8" action="/bigspotteddog/ScrollToFixed/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/bigspotteddog/ScrollToFixed/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <input type="text"
    class="js-site-search-field is-clearable"
    data-hotkey="s"
    name="q"
    placeholder="Search"
    data-global-scope-placeholder="Search GitHub"
    data-repo-scope-placeholder="Search"
    tabindex="1"
    autocapitalize="off">
  <div class="scope-badge">This repository</div>
</form>
    </div>

      <ul class="header-nav left">
          <li class="header-nav-item">
            <a class="header-nav-link" href="/explore" data-ga-click="(Logged out) Header, go to explore, text:explore">Explore</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="/features" data-ga-click="(Logged out) Header, go to features, text:features">Features</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://enterprise.github.com/" data-ga-click="(Logged out) Header, go to enterprise, text:enterprise">Enterprise</a>
          </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="/blog" data-ga-click="(Logged out) Header, go to blog, text:blog">Blog</a>
          </li>
      </ul>

  </div>
</div>



      <div id="start-of-content" class="accessibility-aid"></div>
          <div class="site" itemscope itemtype="http://schema.org/WebPage">
    <div id="js-flash-container">
      
    </div>
    <div class="pagehead repohead instapaper_ignore readability-menu">
      <div class="container">
        
<ul class="pagehead-actions">


  <li>
      <a href="/login?return_to=%2Fbigspotteddog%2FScrollToFixed"
    class="minibutton with-count star-button tooltipped tooltipped-n"
    aria-label="You must be signed in to star a repository" rel="nofollow">
    <span class="octicon octicon-star"></span>
    Star
  </a>

    <a class="social-count js-social-count" href="/bigspotteddog/ScrollToFixed/stargazers">
      849
    </a>

  </li>

    <li>
      <a href="/login?return_to=%2Fbigspotteddog%2FScrollToFixed"
        class="minibutton with-count js-toggler-target fork-button tooltipped tooltipped-n"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <span class="octicon octicon-repo-forked"></span>
        Fork
      </a>
      <a href="/bigspotteddog/ScrollToFixed/network" class="social-count">
        300
      </a>
    </li>
</ul>

        <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public">
          <span class="mega-octicon octicon-repo"></span>
          <span class="author"><a href="/bigspotteddog" class="url fn" itemprop="url" rel="author"><span itemprop="title">bigspotteddog</span></a></span><!--
       --><span class="path-divider">/</span><!--
       --><strong><a href="/bigspotteddog/ScrollToFixed" class="js-current-repository js-repo-home-link">ScrollToFixed</a></strong>

          <span class="page-context-loader">
            <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </span>

        </h1>
      </div><!-- /.container -->
    </div><!-- /.repohead -->

    <div class="container">
      <div class="repository-with-sidebar repo-container new-discussion-timeline  ">
        <div class="repository-sidebar clearfix">
            
<div class="sunken-menu vertical-right repo-nav js-repo-nav js-repository-container-pjax js-octicon-loaders" data-issue-count-url="/bigspotteddog/ScrollToFixed/issues/counts">
  <div class="sunken-menu-contents">
    <ul class="sunken-menu-group">
      <li class="tooltipped tooltipped-w" aria-label="Code">
        <a href="/bigspotteddog/ScrollToFixed" aria-label="Code" class="selected js-selected-navigation-item sunken-menu-item" data-hotkey="g c" data-pjax="true" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /bigspotteddog/ScrollToFixed">
          <span class="octicon octicon-code"></span> <span class="full-word">Code</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

        <li class="tooltipped tooltipped-w" aria-label="Issues">
          <a href="/bigspotteddog/ScrollToFixed/issues" aria-label="Issues" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /bigspotteddog/ScrollToFixed/issues">
            <span class="octicon octicon-issue-opened"></span> <span class="full-word">Issues</span>
            <span class="js-issue-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>        </li>

      <li class="tooltipped tooltipped-w" aria-label="Pull Requests">
        <a href="/bigspotteddog/ScrollToFixed/pulls" aria-label="Pull Requests" class="js-selected-navigation-item sunken-menu-item js-disable-pjax" data-hotkey="g p" data-selected-links="repo_pulls /bigspotteddog/ScrollToFixed/pulls">
            <span class="octicon octicon-git-pull-request"></span> <span class="full-word">Pull Requests</span>
            <span class="js-pull-replace-counter"></span>
            <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>


    </ul>
    <div class="sunken-menu-separator"></div>
    <ul class="sunken-menu-group">

      <li class="tooltipped tooltipped-w" aria-label="Pulse">
        <a href="/bigspotteddog/ScrollToFixed/pulse/weekly" aria-label="Pulse" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="pulse /bigspotteddog/ScrollToFixed/pulse/weekly">
          <span class="octicon octicon-pulse"></span> <span class="full-word">Pulse</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>

      <li class="tooltipped tooltipped-w" aria-label="Graphs">
        <a href="/bigspotteddog/ScrollToFixed/graphs" aria-label="Graphs" class="js-selected-navigation-item sunken-menu-item" data-pjax="true" data-selected-links="repo_graphs repo_contributors /bigspotteddog/ScrollToFixed/graphs">
          <span class="octicon octicon-graph"></span> <span class="full-word">Graphs</span>
          <img alt="" class="mini-loader" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
</a>      </li>
    </ul>


  </div>
</div>

              <div class="only-with-full-nav">
                
  
<div class="clone-url open"
  data-protocol-type="http"
  data-url="/users/set_protocol?protocol_selector=http&amp;protocol_type=clone">
  <h3><span class="text-emphasized">HTTPS</span> clone URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/bigspotteddog/ScrollToFixed.git" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/bigspotteddog/ScrollToFixed.git" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>

  
<div class="clone-url "
  data-protocol-type="subversion"
  data-url="/users/set_protocol?protocol_selector=subversion&amp;protocol_type=clone">
  <h3><span class="text-emphasized">Subversion</span> checkout URL</h3>
  <div class="input-group">
    <input type="text" class="input-mini input-monospace js-url-field"
           value="https://github.com/bigspotteddog/ScrollToFixed" readonly="readonly">
    <span class="input-group-button">
      <button aria-label="Copy to clipboard" class="js-zeroclipboard minibutton zeroclipboard-button" data-clipboard-text="https://github.com/bigspotteddog/ScrollToFixed" data-copied-hint="Copied!" type="button"><span class="octicon octicon-clippy"></span></button>
    </span>
  </div>
</div>


<p class="clone-options">You can clone with
      <a href="#" class="js-clone-selector" data-protocol="http">HTTPS</a>
      or <a href="#" class="js-clone-selector" data-protocol="subversion">Subversion</a>.
  <a href="https://help.github.com/articles/which-remote-url-should-i-use" class="help tooltipped tooltipped-n" aria-label="Get help on which URL is right for you.">
    <span class="octicon octicon-question"></span>
  </a>
</p>


  <a href="http://windows.github.com" class="minibutton sidebar-button" title="Save bigspotteddog/ScrollToFixed to your computer and use it in GitHub Desktop." aria-label="Save bigspotteddog/ScrollToFixed to your computer and use it in GitHub Desktop.">
    <span class="octicon octicon-device-desktop"></span>
    Clone in Desktop
  </a>

                <a href="/bigspotteddog/ScrollToFixed/archive/master.zip"
                   class="minibutton sidebar-button"
                   aria-label="Download the contents of bigspotteddog/ScrollToFixed as a zip file"
                   title="Download the contents of bigspotteddog/ScrollToFixed as a zip file"
                   rel="nofollow">
                  <span class="octicon octicon-cloud-download"></span>
                  Download ZIP
                </a>
              </div>
        </div><!-- /.repository-sidebar -->

        <div id="js-repo-pjax-container" class="repository-content context-loader-container" data-pjax-container>
          

<a href="/bigspotteddog/ScrollToFixed/blob/fdeb277f092fbe04b547c2f225a900f5c09ddf18/jquery-scrolltofixed-min.js" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:9fd74f259cd2e5d2c07a227d805a771f -->

<div class="file-navigation">
  
<div class="select-menu js-menu-container js-select-menu left">
  <span class="minibutton select-menu-button js-menu-target css-truncate" data-hotkey="w"
    data-master-branch="master"
    data-ref="master"
    title="master"
    role="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <span class="octicon octicon-git-branch"></span>
    <i>branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </span>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="select-menu-title">Switch branches/tags</span>
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
      </div> <!-- /.select-menu-header -->

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" class="js-select-menu-tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" class="js-select-menu-tab">Tags</a>
            </li>
          </ul>
        </div><!-- /.select-menu-tabs -->
      </div><!-- /.select-menu-filters -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/blob/gh-pages/jquery-scrolltofixed-min.js"
                 data-name="gh-pages"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="gh-pages">gh-pages</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/blob/ios/jquery-scrolltofixed-min.js"
                 data-name="ios"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="ios">ios</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item selected">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/blob/master/jquery-scrolltofixed-min.js"
                 data-name="master"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="master">master</a>
            </div> <!-- /.select-menu-item -->
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.6/jquery-scrolltofixed-min.js"
                 data-name="1.0.6"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.6">1.0.6</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.5/jquery-scrolltofixed-min.js"
                 data-name="1.0.5"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.5">1.0.5</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.4/jquery-scrolltofixed-min.js"
                 data-name="1.0.4"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.4">1.0.4</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.3/jquery-scrolltofixed-min.js"
                 data-name="1.0.3"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.3">1.0.3</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.2/jquery-scrolltofixed-min.js"
                 data-name="1.0.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.2">1.0.2</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.1/jquery-scrolltofixed-min.js"
                 data-name="1.0.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.1">1.0.1</a>
            </div> <!-- /.select-menu-item -->
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/bigspotteddog/ScrollToFixed/tree/1.0.0/jquery-scrolltofixed-min.js"
                 data-name="1.0.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.0">1.0.0</a>
            </div> <!-- /.select-menu-item -->
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div> <!-- /.select-menu-list -->

    </div> <!-- /.select-menu-modal -->
  </div> <!-- /.select-menu-modal-holder -->
</div> <!-- /.select-menu -->

  <div class="button-group right">
    <a href="/bigspotteddog/ScrollToFixed/find/master"
          class="js-show-file-finder minibutton empty-icon tooltipped tooltipped-s"
          data-pjax
          data-hotkey="t"
          aria-label="Quickly jump between files">
      <span class="octicon octicon-list-unordered"></span>
    </a>
    <button class="js-zeroclipboard minibutton zeroclipboard-button"
          data-clipboard-text="jquery-scrolltofixed-min.js"
          aria-label="Copy to clipboard"
          data-copied-hint="Copied!">
      <span class="octicon octicon-clippy"></span>
    </button>
  </div>

  <div class="breadcrumb">
    <span class='repo-root js-repo-root'><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/bigspotteddog/ScrollToFixed" class="" data-branch="master" data-direction="back" data-pjax="true" itemscope="url"><span itemprop="title">ScrollToFixed</span></a></span></span><span class="separator"> / </span><strong class="final-path">jquery-scrolltofixed-min.js</strong>
  </div>
</div>


  <div class="commit file-history-tease">
    <div class="file-history-tease-header">
        <img alt="bigspotteddog" class="avatar" data-user="865101" height="24" src="https://avatars0.githubusercontent.com/u/865101?v=2&amp;s=48" width="24" />
        <span class="author"><a href="/bigspotteddog" rel="author">bigspotteddog</a></span>
        <time datetime="2014-06-11T20:30:49-07:00" is="relative-time">June 11, 2014</time>
        <div class="commit-title">
            <a href="/bigspotteddog/ScrollToFixed/commit/d848da89a3657da2e6b8f4c73490d328a4c44990" class="message" data-pjax="true" title="See #146: Minified.">See</a> <a href="https://github.com/bigspotteddog/ScrollToFixed/pull/146" class="issue-link" title="Handle touchemove events">#146</a><a href="/bigspotteddog/ScrollToFixed/commit/d848da89a3657da2e6b8f4c73490d328a4c44990" class="message" data-pjax="true" title="See #146: Minified.">: Minified.</a>
        </div>
    </div>

    <div class="participation">
      <p class="quickstat">
        <a href="#blob_contributors_box" rel="facebox">
          <strong>3</strong>
           contributors
        </a>
      </p>
          <a class="avatar-link tooltipped tooltipped-s" aria-label="bigspotteddog" href="/bigspotteddog/ScrollToFixed/commits/master/jquery-scrolltofixed-min.js?author=bigspotteddog"><img alt="bigspotteddog" class="avatar" data-user="865101" height="20" src="https://avatars2.githubusercontent.com/u/865101?v=2&amp;s=40" width="20" /></a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="jwoldan" href="/bigspotteddog/ScrollToFixed/commits/master/jquery-scrolltofixed-min.js?author=jwoldan"><img alt="jwoldan" class="avatar" data-user="611085" height="20" src="https://avatars1.githubusercontent.com/u/611085?v=2&amp;s=40" width="20" /></a>
    <a class="avatar-link tooltipped tooltipped-s" aria-label="DukeBG" href="/bigspotteddog/ScrollToFixed/commits/master/jquery-scrolltofixed-min.js?author=DukeBG"><img alt="DukeBG" class="avatar" data-user="5087584" height="20" src="https://avatars1.githubusercontent.com/u/5087584?v=2&amp;s=40" width="20" /></a>


    </div>
    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list">
          <li class="facebox-user-list-item">
            <img alt="bigspotteddog" data-user="865101" height="24" src="https://avatars0.githubusercontent.com/u/865101?v=2&amp;s=48" width="24" />
            <a href="/bigspotteddog">bigspotteddog</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="jwoldan" data-user="611085" height="24" src="https://avatars3.githubusercontent.com/u/611085?v=2&amp;s=48" width="24" />
            <a href="/jwoldan">jwoldan</a>
          </li>
          <li class="facebox-user-list-item">
            <img alt="DukeBG" data-user="5087584" height="24" src="https://avatars3.githubusercontent.com/u/5087584?v=2&amp;s=48" width="24" />
            <a href="/DukeBG">DukeBG</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file-box">
  <div class="file">
    <div class="meta clearfix">
      <div class="info file-name">
          <span>1 lines (1 sloc)</span>
          <span class="meta-divider"></span>
        <span>5.765 kb</span>
      </div>
      <div class="actions">
        <div class="button-group">
          <a href="/bigspotteddog/ScrollToFixed/raw/master/jquery-scrolltofixed-min.js" class="minibutton " id="raw-url">Raw</a>
            <a href="/bigspotteddog/ScrollToFixed/blame/master/jquery-scrolltofixed-min.js" class="minibutton js-update-url-with-hash">Blame</a>
          <a href="/bigspotteddog/ScrollToFixed/commits/master/jquery-scrolltofixed-min.js" class="minibutton " rel="nofollow">History</a>
        </div><!-- /.button-group -->

          <a class="octicon-button tooltipped tooltipped-nw"
             href="http://windows.github.com" aria-label="Open this file in GitHub for Windows">
              <span class="octicon octicon-device-desktop"></span>
          </a>

            <a class="octicon-button disabled tooltipped tooltipped-w" href="#"
               aria-label="You must be signed in to make or propose changes"><span class="octicon octicon-pencil"></span></a>

          <a class="octicon-button danger disabled tooltipped tooltipped-w" href="#"
             aria-label="You must be signed in to make or propose changes">
          <span class="octicon octicon-trashcan"></span>
        </a>
      </div><!-- /.actions -->
    </div>
      
  <div class="blob-wrapper data type-javascript">
      <table class="highlight tab-size-8 js-file-line-container">
      <tr>
        <td id="L1" class="blob-num js-line-number" data-line-number="1"></td>
        <td id="LC1" class="blob-code js-file-line">(function(a){a.isScrollToFixed=function(b){return !!a(b).data(&quot;ScrollToFixed&quot;)};a.ScrollToFixed=function(d,i){var l=this;l.$el=a(d);l.el=d;l.$el.data(&quot;ScrollToFixed&quot;,l);var c=false;var G=l.$el;var H;var E;var e;var y;var D=0;var q=0;var j=-1;var f=-1;var t=null;var z;var g;function u(){G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;);f=-1;D=G.offset().top;q=G.offset().left;if(l.options.offsets){q+=(G.offset().left-G.position().left)}if(j==-1){j=q}H=G.css(&quot;position&quot;);c=true;if(l.options.bottom!=-1){G.trigger(&quot;preFixed.ScrollToFixed&quot;);w();G.trigger(&quot;fixed.ScrollToFixed&quot;)}}function n(){var I=l.options.limit;if(!I){return 0}if(typeof(I)===&quot;function&quot;){return I.apply(G)}return I}function p(){return H===&quot;fixed&quot;}function x(){return H===&quot;absolute&quot;}function h(){return !(p()||x())}function w(){if(!p()){t.css({display:G.css(&quot;display&quot;),width:G.outerWidth(true),height:G.outerHeight(true),&quot;float&quot;:G.css(&quot;float&quot;)});cssOptions={&quot;z-index&quot;:l.options.zIndex,position:&quot;fixed&quot;,top:l.options.bottom==-1?s():&quot;&quot;,bottom:l.options.bottom==-1?&quot;&quot;:l.options.bottom,&quot;margin-left&quot;:&quot;0px&quot;};if(!l.options.dontSetWidth){cssOptions.width=G.width()}G.css(cssOptions);G.addClass(l.options.baseClassName);if(l.options.className){G.addClass(l.options.className)}H=&quot;fixed&quot;}}function b(){var J=n();var I=q;if(l.options.removeOffsets){I=&quot;&quot;;J=J-D}cssOptions={position:&quot;absolute&quot;,top:J,left:I,&quot;margin-left&quot;:&quot;0px&quot;,bottom:&quot;&quot;};if(!l.options.dontSetWidth){cssOptions.width=G.width()}G.css(cssOptions);H=&quot;absolute&quot;}function k(){if(!h()){f=-1;t.css(&quot;display&quot;,&quot;none&quot;);G.css({&quot;z-index&quot;:y,width:&quot;&quot;,position:E,left:&quot;&quot;,top:e,&quot;margin-left&quot;:&quot;&quot;});G.removeClass(&quot;scroll-to-fixed-fixed&quot;);if(l.options.className){G.removeClass(l.options.className)}H=null}}function v(I){if(I!=f){G.css(&quot;left&quot;,q-I);f=I}}function s(){var I=l.options.marginTop;if(!I){return 0}if(typeof(I)===&quot;function&quot;){return I.apply(G)}return I}function A(){if(!a.isScrollToFixed(G)){return}var K=c;if(!c){u()}else{if(h()){D=G.offset().top;q=G.offset().left}}var I=a(window).scrollLeft();var L=a(window).scrollTop();var J=n();if(l.options.minWidth&amp;&amp;a(window).width()&lt;l.options.minWidth){if(!h()||!K){o();G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;)}}else{if(l.options.maxWidth&amp;&amp;a(window).width()&gt;l.options.maxWidth){if(!h()||!K){o();G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;)}}else{if(l.options.bottom==-1){if(J&gt;0&amp;&amp;L&gt;=J-s()){if(!x()||!K){o();G.trigger(&quot;preAbsolute.ScrollToFixed&quot;);b();G.trigger(&quot;unfixed.ScrollToFixed&quot;)}}else{if(L&gt;=D-s()){if(!p()||!K){o();G.trigger(&quot;preFixed.ScrollToFixed&quot;);w();f=-1;G.trigger(&quot;fixed.ScrollToFixed&quot;)}v(I)}else{if(!h()||!K){o();G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;)}}}}else{if(J&gt;0){if(L+a(window).height()-G.outerHeight(true)&gt;=J-(s()||-m())){if(p()){o();G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);if(E===&quot;absolute&quot;){b()}else{k()}G.trigger(&quot;unfixed.ScrollToFixed&quot;)}}else{if(!p()){o();G.trigger(&quot;preFixed.ScrollToFixed&quot;);w()}v(I);G.trigger(&quot;fixed.ScrollToFixed&quot;)}}else{v(I)}}}}}function m(){if(!l.options.bottom){return 0}return l.options.bottom}function o(){var I=G.css(&quot;position&quot;);if(I==&quot;absolute&quot;){G.trigger(&quot;postAbsolute.ScrollToFixed&quot;)}else{if(I==&quot;fixed&quot;){G.trigger(&quot;postFixed.ScrollToFixed&quot;)}else{G.trigger(&quot;postUnfixed.ScrollToFixed&quot;)}}}var C=function(I){if(G.is(&quot;:visible&quot;)){c=false;A()}};var F=function(I){(!!window.requestAnimationFrame)?requestAnimationFrame(A):A()};var B=function(){var J=document.body;if(document.createElement&amp;&amp;J&amp;&amp;J.appendChild&amp;&amp;J.removeChild){var L=document.createElement(&quot;div&quot;);if(!L.getBoundingClientRect){return null}L.innerHTML=&quot;x&quot;;L.style.cssText=&quot;position:fixed;top:100px;&quot;;J.appendChild(L);var M=J.style.height,N=J.scrollTop;J.style.height=&quot;3000px&quot;;J.scrollTop=500;var I=L.getBoundingClientRect().top;J.style.height=M;var K=(I===100);J.removeChild(L);J.scrollTop=N;return K}return null};var r=function(I){I=I||window.event;if(I.preventDefault){I.preventDefault()}I.returnValue=false};l.init=function(){l.options=a.extend({},a.ScrollToFixed.defaultOptions,i);y=G.css(&quot;z-index&quot;);l.$el.css(&quot;z-index&quot;,l.options.zIndex);t=a(&quot;&lt;div /&gt;&quot;);H=G.css(&quot;position&quot;);E=G.css(&quot;position&quot;);e=G.css(&quot;top&quot;);if(h()){l.$el.after(t)}a(window).bind(&quot;resize.ScrollToFixed&quot;,C);a(window).bind(&quot;scroll.ScrollToFixed&quot;,F);if(&quot;ontouchmove&quot; in window){a(window).bind(&quot;touchmove.ScrollToFixed&quot;,A)}if(l.options.preFixed){G.bind(&quot;preFixed.ScrollToFixed&quot;,l.options.preFixed)}if(l.options.postFixed){G.bind(&quot;postFixed.ScrollToFixed&quot;,l.options.postFixed)}if(l.options.preUnfixed){G.bind(&quot;preUnfixed.ScrollToFixed&quot;,l.options.preUnfixed)}if(l.options.postUnfixed){G.bind(&quot;postUnfixed.ScrollToFixed&quot;,l.options.postUnfixed)}if(l.options.preAbsolute){G.bind(&quot;preAbsolute.ScrollToFixed&quot;,l.options.preAbsolute)}if(l.options.postAbsolute){G.bind(&quot;postAbsolute.ScrollToFixed&quot;,l.options.postAbsolute)}if(l.options.fixed){G.bind(&quot;fixed.ScrollToFixed&quot;,l.options.fixed)}if(l.options.unfixed){G.bind(&quot;unfixed.ScrollToFixed&quot;,l.options.unfixed)}if(l.options.spacerClass){t.addClass(l.options.spacerClass)}G.bind(&quot;resize.ScrollToFixed&quot;,function(){t.height(G.height())});G.bind(&quot;scroll.ScrollToFixed&quot;,function(){G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;);A()});G.bind(&quot;detach.ScrollToFixed&quot;,function(I){r(I);G.trigger(&quot;preUnfixed.ScrollToFixed&quot;);k();G.trigger(&quot;unfixed.ScrollToFixed&quot;);a(window).unbind(&quot;resize.ScrollToFixed&quot;,C);a(window).unbind(&quot;scroll.ScrollToFixed&quot;,F);G.unbind(&quot;.ScrollToFixed&quot;);t.remove();l.$el.removeData(&quot;ScrollToFixed&quot;)});C()};l.init()};a.ScrollToFixed.defaultOptions={marginTop:0,limit:0,bottom:-1,zIndex:1000,baseClassName:&quot;scroll-to-fixed-fixed&quot;};a.fn.scrollToFixed=function(b){return this.each(function(){(new a.ScrollToFixed(this,b))})}})(jQuery);</td>
      </tr>
</table>

  </div>

  </div>
</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <form accept-charset="UTF-8" class="js-jump-to-line-form">
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" autofocus>
    <button type="submit" class="button">Go</button>
  </form>
</div>

        </div>

      </div><!-- /.repo-container -->
      <div class="modal-backdrop"></div>
    </div><!-- /.container -->
  </div><!-- /.site -->


    </div><!-- /.wrapper -->

      <div class="container">
  <div class="site-footer">
    <ul class="site-footer-links right">
      <li><a href="https://status.github.com/">Status</a></li>
      <li><a href="http://developer.github.com">API</a></li>
      <li><a href="http://training.github.com">Training</a></li>
      <li><a href="http://shop.github.com">Shop</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>

    </ul>

    <a href="/" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
    </a>

    <ul class="site-footer-links">
      <li>&copy; 2014 <span title="0.02200s from github-fe126-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="/site/terms">Terms</a></li>
        <li><a href="/site/privacy">Privacy</a></li>
        <li><a href="/security">Security</a></li>
        <li><a href="/contact">Contact</a></li>
    </ul>
  </div><!-- /.site-footer -->
</div><!-- /.container -->


    <div class="fullscreen-overlay js-fullscreen-overlay" id="fullscreen_overlay">
  <div class="fullscreen-container js-suggester-container">
    <div class="textarea-wrap">
      <textarea name="fullscreen-contents" id="fullscreen-contents" class="fullscreen-contents js-fullscreen-contents js-suggester-field" placeholder=""></textarea>
    </div>
  </div>
  <div class="fullscreen-sidebar">
    <a href="#" class="exit-fullscreen js-exit-fullscreen tooltipped tooltipped-w" aria-label="Exit Zen Mode">
      <span class="mega-octicon octicon-screen-normal"></span>
    </a>
    <a href="#" class="theme-switcher js-theme-switcher tooltipped tooltipped-w"
      aria-label="Switch themes">
      <span class="octicon octicon-color-mode"></span>
    </a>
  </div>
</div>



    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <a href="#" class="octicon octicon-x close js-ajax-error-dismiss" aria-label="Dismiss error"></a>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-bc28a4f6b05fd6cd91bbc92310bbbc53e54c6ec2.js" type="text/javascript"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-1d4c97a5d7662f40cd45545e25f18281f5b6ef5c.js" type="text/javascript"></script>
      
      
        <script async src="https://www.google-analytics.com/analytics.js"></script>
  </body>
</html>

