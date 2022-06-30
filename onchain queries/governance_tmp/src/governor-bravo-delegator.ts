import {
    VoteCast as VoteCastEvent,
    NewImplementation as NewImplementationEvent,
    ProposalCreated as ProposalCreatedEvent
} from "../generated/GovernorBravoDelegator/GovernorBravoDelegator"
import { Proposal, Votes, Implementation } from "../generated/schema"


export function handleProposalCreated(event: ProposalCreatedEvent): void{
    let Id = event.params.id; 
    let proposal = Proposal.load(Id.toString());
    if (proposal == null){
        proposal = new Proposal(Id.toString());
        proposal.blocktime = event.block.timestamp
    }
    proposal.save();
}


export function handleVoteCast(event: VoteCastEvent): void {
    let voterId = event.params.voter;
    let proposalId = event.params.proposalId;

    let vote = Votes.load(proposalId.toHexString() + "-" + voterId.toHexString());
    if (vote == null){
        vote = new Votes(proposalId.toHexString() + "-" + voterId.toHexString());
        vote.voter = voterId;
        let single_vote = event.params.votes;
        vote.single_vote = single_vote;
        vote.proposalID = event.params.proposalId.toString();
    }
    vote.save();

    let proposal = Proposal.load(proposalId.toString());
    if (proposal == null){
        proposal = new Proposal(proposalId.toString());
    }

    // proposal.voter = event.params.voter;
    // proposal.votes = event.params.votes;
    proposal.save();
}

export function handleNewImplementation(event: NewImplementationEvent): void{
    let oldId = event.params.oldImplementation;
    let implementation = Implementation.load(oldId.toHexString());
    if (implementation == null){
        implementation = new Implementation(oldId.toHexString());
        implementation.newImplementation = event.params.newImplementation
        implementation.blocktime = event.block.timestamp
    }
    implementation.save();
}
