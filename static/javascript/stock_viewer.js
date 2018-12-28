

function change_symbol()
{
    var symbol = document.getElementById("symbol_input").value.toUpperCase();
    if(symbol)
    {
        document.getElementById('stock_title').innerHTML = `<font color="#27e2e2">Loading symbol ${symbol}...</font>`;

        var compact = document.getElementById('compact_checkbox').checked;
        var url = `/stock_data?symbol=${symbol}&format=line&compact=${compact}`;
        var xmlHttp = new XMLHttpRequest(); 
        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState === 4 && xmlHttp.status === 200)
            {
                var data = JSON.parse(xmlHttp.response);
                draw_plot(data, symbol);
            }
            else if(xmlHttp.readyState === 4 && xmlHttp.status === 404)
            {
                document.getElementById('stock_title').innerHTML = '<font color="red">Symbol not found</font>';
            }
        };
        xmlHttp.open("GET", url, true );
        xmlHttp.send(null);
    }
}

function draw_plot(data, symbol)
{
    var layout = {
        dragmode: 'zoom', 
        margin: {
            r: 10, 
            t: 25, 
            b: 40, 
            l: 60
        }, 
        showlegend: false, 
        xaxis: {
            autorange: true,  
            title: 'Date', 
            type: 'date'
        }, 
        yaxis: {
            autorange: true, 
            type: 'linear'
        }
        };

        document.getElementById('stock_title').innerHTML = symbol;
        Plotly.react('graph_holder', data, layout);
}