function simulateNetworkDelay() {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve('Network delay simulated');
        }, 2000);
    });
}

console.log('Starting delay');
simulateNetworkDelay().then(function(result) {
    console.log(result);
    console.log('Delay finished');
});

async function testAsynWait() {
    console.log('Starting async/awaint delay');
    const result = await simulateNetworkDelay();
    console.log(result);
    console.log('Async/await delay finished');
}

testAsynWait();