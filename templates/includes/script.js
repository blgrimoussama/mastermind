setInterval( function() {
    fetch('/data_json').then(
        response => response.json()
    ).then(
        data =>
            data.forEach(match => 
                updateElement(match)
            )
        
    )
}, 1000
);

function updateElement(match) {
Object.entries(match).forEach(([k,v]) => {
    element = document.getElementById(k + '_' + match.id);
    // Get Previous value first
    previousValue = element.innerHTML;

    // If Previous value is not equal to the new value, change it!
    if (previousValue !== v.toString()) {
        element.innerHTML = v.toString();
    }
})
}


setInterval( function() {
    fetch('/mastermind_json').then(
        response => response.json()
    ).then(
        data =>
            data.forEach(column => 
                column.forEach(row => 
                    updateCircleColor(column, row))
            )
        
    )
}, 1000
);

function updateCircleColor(column, row) { // Row means also Color
    console.log(column, row);
    circle = document.getElementById('circle_' + column + '_' + column.indexof(row));
    
    previousValue = element.innerHTML;

    // If Previous value is not equal to the new value, change it!
    if (previousValue !== v.toString()) {
        circle.style.fill = row;
    }
}