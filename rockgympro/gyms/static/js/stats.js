$.get("stats.json").success(function(data){
    items = ["setters", "types", "bouldering_grades", "top_rope_grades", "locations"]
    for(var i = 0;i<5;i++){
        var item = items[i]
        chartOptions = {        
            series: {
                pie: {
                    show: true,  
                    innerRadius: .5, 
                    stroke: {
                        width: 4
                    }
                }
            }, 
                
            legend: {
                position: 'ne'
            }, 
            
            tooltip: true,

            tooltipOpts: {
                content: '%s: %y'
            },
            
            grid: {
                hoverable: true
            },

            colors: App.chartColors
        };
        var holder = $('#'+item+'-chart');
        if (holder.length) {
            $.plot(holder, data[item], chartOptions );
        }
    }
    
})
