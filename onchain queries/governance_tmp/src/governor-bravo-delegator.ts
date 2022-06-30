import {
  VoteCast as VoteCastEvent
} from "../generated/GovernorBravoDelegator/GovernorBravoDelegator"
import { Proposal, Votes } from "../generated/schema"

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


