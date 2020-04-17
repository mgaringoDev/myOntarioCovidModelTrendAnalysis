---
layout: page
---



<div class="float-left">
<div class="recentpost" style="padding: 10px; font-size: small;height: 250px;overflow-y: scroll;">
<div id="inline_toc" markdown="1">
<h4>Table of Contents</h4>
* TOC
{:toc}
</div>
</div>
</div>




# Introduction
I wanted to get a deeper insight on the current state of things here in Ontario.  This is by no means a comprehensive look at all possible models but only the models that I have come across through my readings.

# Data Set
Berry I, Soucy J-PR, Tuite A, Fisman D. Open access epidemiologic data and an interactive dashboard to monitor the COVID-19 outbreak in Canada. CMAJ. 2020 Apr 14;192(15):E420.

# To Do:

- Trend Analysis:
    - [x] Log Regression
    - [x] fbProphet

- Model Creation:
    - [x] SIR(M)
    - [x] SAIR(M)
    - [x] SDIR(M)
    - [x] SIGR(M)
    - [x] SEIR(M)

- Prediction:
    - [ ] 


# Order of Reading

## [Looking at Growth Rates](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/GrowthFactor.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/weeklyGrowthFactor.PNG)

## [Looking at Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/TrendLines_fbprophet.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/trendAnalysis_1.PNG)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/trendAnalysis_2.PNG)

These are the critical dates from the above graph.

![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/criticalDates.PNG)

## [Modeling Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/ModelComparison.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/3PhaseModelComparison.PNG)


## [Comapring Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/ModelComparison.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/entireTimeModelComparison.PNG)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/modelErrorComparison.png)


{% for post in paginator.posts %}
<div class="post-preview">
    <a href="{{ post.url | prepend: site.baseurl }}">
        <h2 class="post-title">            {{ post.title }}
        </h2>
        {% if post.subtitle %}
        <h3 class="post-subtitle">
            {{ post.subtitle }}
        </h3>
        {% endif %}
    </a>
    <p class="post-meta" style="margin-bottom:5px">Posted by {{ post.author }} on {{ post.date | date: "%B %-d, %Y" }}</p>
    <div class="notepad-index-post-tags" style="">
        {% for tag in post.tags %}<a href="{{ site.baseurl }}/search/index.html#{{ tag | cgi_encode }}" title="Other posts from the {{ tag | capitalize }} tag">{{ tag | capitalize }}</a>{% unless forloop.last %}&nbsp;{% endunless %}{% endfor %}
    </div>
</div>
<hr>
{% endfor %}

<!-- Pager -->
{% if paginator.total_pages > 1 %}
<ul class="pager">
    {% if paginator.previous_page == 1 %}
    <li class="previous">
        <a href="{{site.baseurl}}/index.html">&larr; Newer Posts</a>
    </li>
    {% elsif paginator.previous_page %}
    <li class="previous">
        <a href="{{site.baseurl}}/page{{paginator.previous_page}}/index.html">&larr; Newer Posts</a>
    </li>
    {% endif %}

    {% if paginator.next_page %}
    <li class="next">
        <a href="{{site.baseurl}}/page{{paginator.next_page}}/index.html">Older Posts &rarr;</a>
    </li>
    {% endif %}
</ul>
{% endif %}

