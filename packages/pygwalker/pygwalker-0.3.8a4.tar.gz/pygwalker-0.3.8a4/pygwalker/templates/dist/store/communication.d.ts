import { ICommunication } from '../utils/communication';
declare class CommunicationStore {
    comm: ICommunication | null;
    setComm(comm: ICommunication): void;
    constructor();
}
declare const communicationStore: CommunicationStore;
export default communicationStore;
