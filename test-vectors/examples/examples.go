package examples

import (
	"crypto/ed25519"

	hiveEd25519 "github.com/iotaledger/hive.go/crypto/ed25519"
	"github.com/iotaledger/hive.go/lo"
	iotago "github.com/iotaledger/iota.go/v4"
	"github.com/iotaledger/iota.go/v4/builder"
	"github.com/iotaledger/iota.go/v4/tpkg"
)

func SignedTransaction(api iotago.API) *iotago.SignedTransaction {
	keyPair := hiveEd25519.GenerateKeyPair()
	addr := iotago.Ed25519AddressFromPubKey(keyPair.PublicKey[:])

	output1 := &iotago.BasicOutput{
		Amount: 100000,
		UnlockConditions: iotago.BasicOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.BasicOutputFeatures{
			tpkg.RandNativeTokenFeature(),
		},
	}

	output2 := &iotago.AccountOutput{
		Amount: 100000,
		Mana:   5000,
		UnlockConditions: iotago.AccountOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.AccountOutputFeatures{
			&iotago.StateMetadataFeature{
				Entries: iotago.StateMetadataFeatureEntries{
					"hello": []byte("world"),
				},
			},
		},
	}

	creationSlot := iotago.SlotIndex(1 << 20)
	tx := lo.PanicOnErr(builder.NewTransactionBuilder(api).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      tpkg.RandOutputID(0),
			Input:        output1,
		}).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      tpkg.RandOutputID(0),
			Input:        output2,
		}).
		AddOutput(output1).
		AddOutput(output2).
		AddCommitmentInput(&iotago.CommitmentInput{CommitmentID: iotago.NewCommitmentID(85, tpkg.Rand32ByteArray())}).
		AddBlockIssuanceCreditInput(&iotago.BlockIssuanceCreditInput{AccountID: tpkg.RandAccountID()}).
		AddRewardInput(&iotago.RewardInput{Index: 0}, 50).
		IncreaseAllotment(tpkg.RandAccountID(), tpkg.RandMana(10000)+1).
		IncreaseAllotment(tpkg.RandAccountID(), tpkg.RandMana(10000)+1).
		WithTransactionCapabilities(
			iotago.TransactionCapabilitiesBitMaskWithCapabilities(iotago.WithTransactionCanBurnNativeTokens(true)),
		).
		SetCreationSlot(creationSlot).
		Build(iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})))

	return tx
}

func BasicBlockWithTransaction(api iotago.API, payload iotago.ApplicationPayload) *iotago.Block {
	keyPair := hiveEd25519.GenerateKeyPair()

	randIdentifier := tpkg.Rand32ByteArray()
	randCommitmentID := iotago.CommitmentID(append(randIdentifier[:], lo.PanicOnErr(tpkg.RandSlot().Bytes())...))

	return lo.PanicOnErr(builder.NewBasicBlockBuilder(api).
		StrongParents(tpkg.SortedRandBlockIDs(6)).
		MaxBurnedMana(tpkg.RandMana(1000)).
		Payload(payload).
		SlotCommitmentID(randCommitmentID).
		LatestFinalizedSlot(500).
		Sign(tpkg.RandAccountID(), keyPair.PrivateKey[:]).
		Build())
}

func ValidationBlock(api iotago.API) *iotago.Block {
	keyPair := hiveEd25519.GenerateKeyPair()

	randIdentifier := tpkg.Rand32ByteArray()
	randCommitmentID := iotago.CommitmentID(append(randIdentifier[:], lo.PanicOnErr(tpkg.RandSlot().Bytes())...))

	return lo.PanicOnErr(builder.NewValidationBlockBuilder(api).
		StrongParents(tpkg.SortedRandBlockIDs(6)).
		SlotCommitmentID(randCommitmentID).
		LatestFinalizedSlot(500).
		HighestSupportedVersion(api.ProtocolParameters().Version()).
		ProtocolParametersHash(lo.PanicOnErr(api.ProtocolParameters().Hash())).
		Sign(tpkg.RandAccountID(), keyPair.PrivateKey[:]).
		Build())
}
