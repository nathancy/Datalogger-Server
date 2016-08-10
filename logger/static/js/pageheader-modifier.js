function getclick(element)
{
    element.style.backgroundColor = '#9932CC';
}

/* Controls background color when user is on specific page/tab */
$(function() {
    if($('h2').is('#header-color1')){
        var x = document.querySelector(".frontpage-header1");
        x.style.backgroundColor = "#4ACF50";
    }
});

$(function() {
    if($('h2').is('#header-color2')){
        var x = document.querySelector(".frontpage-header2");
        x.style.backgroundColor = "#4ACF50";
    }
});

$(function() {
    if($('h2').is('#header-color3')){
        var x = document.querySelector(".frontpage-header3");
        x.style.backgroundColor = "#4ACF50";
    }
});

/*
$(function(){
    $('.frontpage-header1').click(function(){
        $('.frontpage-header1 .active').removeClass('active');
            $(this).addClass('active');
            });
});

$(function(){
    $('.frontpage-header2').click(function(){
        $('.frontpage-header2 .active').removeClass('active');
            $(this).addClass('active');
            });
});
$(function(){
    $('.frontpage-header3').click(function(){
        $('.frontpage-header3 .active').removeClass('active');
            $(this).addClass('active');
            });
});
$(function(){
    $('.frontpage-header4').click(function(){
        $('.frontpage-header4 .active').removeClass('active');
            $(this).addClass('active');
            });
});
*/
