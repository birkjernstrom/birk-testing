const { SdkClient } = require('memanto-sdk');

async function verifyCrossProcessPersistence() {
    const syncAgentId = 'sys_eng_prod_01';
    const persistenceClient = new SdkClient();

    // Verify state written by Python process
    const currentState = await persistenceClient.get(`${syncAgentId}:status`);
    
    const sessionConfig = {
        syncAgentId,
        timestamp: Date.now()
    };

    console.log(`Cross-process state verification: ${currentState}`);
    
    if (currentState === 'active') {
        console.log('Persistence verified: State consistency maintained across processes.');
    } else {
        process.exit(1);
    }
}

verifyCrossProcessPersistence().catch(console.error);
