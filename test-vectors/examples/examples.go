package examples

import (
	"crypto/ed25519"
	"math/big"
	"time"

	hiveEd25519 "github.com/iotaledger/hive.go/crypto/ed25519"
	"github.com/iotaledger/hive.go/lo"
	iotago "github.com/iotaledger/iota.go/v4"
	"github.com/iotaledger/iota.go/v4/builder"
	"github.com/iotaledger/iota.go/v4/hexutil"
)

var (
	commitmentID = iotago.MustCommitmentIDFromHexString("0x3a1e3b617060146e0362361a4b752833186108395f3b2b3d3e6c655e287d70767ea58d2a")
	issuerID     = iotago.MustAccountIDFromHexString("0x17432c5a7a672503480241125e3952414a7a320441080c624c264b004e09614a")
	privateKey   = lo.Return1(hiveEd25519.PrivateKeyFromBytes(lo.PanicOnErr(hexutil.DecodeHex(
		"0x9396e0257e40961ae310777a3d12d3fe1f6811eeb073d169d538d50753c68eb82daefbcbadd044da470acd2f7fcf6fcb04b873cc801e7ee408018e1dfa0257ac",
	))))
	keyPair = hiveEd25519.KeyPair{
		PrivateKey: privateKey,
		PublicKey:  privateKey.Public(),
	}
)

func SignedTransaction(api iotago.API) *iotago.SignedTransaction {
	addr := iotago.Ed25519AddressFromPubKey(keyPair.PublicKey[:])

	output1 := &iotago.BasicOutput{
		Amount: 100000,
		UnlockConditions: iotago.BasicOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.BasicOutputFeatures{
			&iotago.NativeTokenFeature{
				ID: iotago.NativeTokenID(lo.PanicOnErr(hexutil.DecodeHex(
					"0x086372557616532f714f104e5f44297b7a286d077956291a6d4f59081f484463712a64300c00",
				))),
				Amount: new(big.Int).SetUint64(0x14be8149371263f4),
			},
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

	tx := lo.PanicOnErr(builder.NewTransactionBuilder(api).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      iotago.MustOutputIDFromHexString("0xf09d3cd648a7246c7c1b2ba2f9182465ae5742b78c592392b4b455ab8ed71952000000000000"),
			Input:        output1,
		}).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      iotago.MustOutputIDFromHexString("0xd2c5ccba12b6fad51652131289867492799c9fc5710244418aa6e955f8fa8261000000000000"),
			Input:        output2,
		}).
		AddOutput(output1).
		AddOutput(output2).
		AddCommitmentInput(&iotago.CommitmentInput{CommitmentID: commitmentID}).
		AddBlockIssuanceCreditInput(&iotago.BlockIssuanceCreditInput{AccountID: issuerID}).
		AddRewardInput(&iotago.RewardInput{Index: 0}, 50).
		IncreaseAllotment(
			iotago.MustAccountIDFromHexString("0x7e0d0a5848362b23120f55115b096774036d7610137a631413221f5573344507"),
			2285,
		).
		IncreaseAllotment(
			iotago.MustAccountIDFromHexString("0x476820096e7038107d071a4e473f1e295f346e2d0824263e5e3e7d004f6b6915"),
			2189,
		).
		WithTransactionCapabilities(
			iotago.TransactionCapabilitiesBitMaskWithCapabilities(iotago.WithTransactionCanBurnNativeTokens(true)),
		).
		SetCreationSlot(iotago.SlotIndex(1 << 20)).
		Build(iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})))

	return tx
}

func BasicBlockWithPayload(api iotago.API, payload iotago.ApplicationPayload) *iotago.Block {
	return lo.PanicOnErr(builder.NewBasicBlockBuilder(api).
		StrongParents(iotago.BlockIDs{
			iotago.MustBlockIDFromHexString("0x27e0461873f37040c9e59c35ad8a106fa1b94f5ec9ef89499b31904f9a3de59be58dd44a"),
			iotago.MustBlockIDFromHexString("0x714821f8f257e0a502b71ac7ee57530bb9dc29fe12ff3936f925b835a297680400b76948"),
			iotago.MustBlockIDFromHexString("0x9951e512546cd9c9fbdab348b6cba91a601a29b50854e55a6e14f6803ca1d81ac7eff5ce"),
			iotago.MustBlockIDFromHexString("0xaaa7bacf26f1aa4754d42edeab45d6169ea723b7fdf0f6ff3b6ebe90d09dbff6bc553936"),
			iotago.MustBlockIDFromHexString("0xba75a143de4ac932986fbe7b1d78f639bc6ee8aee10d510d41572851530be884778052aa"),
			iotago.MustBlockIDFromHexString("0xea5315941f4337752905599710b55e64018c71f4d8f299d0636d50484d05e6ac5667b503"),
		}).
		MaxBurnedMana(864).
		Payload(payload).
		SlotCommitmentID(commitmentID).
		LatestFinalizedSlot(500).
		IssuingTime(api.TimeProvider().GenesisTime().Add(30*time.Second)).
		Sign(
			issuerID,
			keyPair.PrivateKey[:],
		).
		Build())
}

func ValidationBlock(api iotago.API) *iotago.Block {
	return lo.PanicOnErr(builder.NewValidationBlockBuilder(api).
		StrongParents(
			iotago.BlockIDs{
				iotago.MustBlockIDFromHexString("0x27e0461873f37040c9e59c35ad8a106fa1b94f5ec9ef89499b31904f9a3de59be58dd44a"),
				iotago.MustBlockIDFromHexString("0x714821f8f257e0a502b71ac7ee57530bb9dc29fe12ff3936f925b835a297680400b76948"),
				iotago.MustBlockIDFromHexString("0x9951e512546cd9c9fbdab348b6cba91a601a29b50854e55a6e14f6803ca1d81ac7eff5ce"),
				iotago.MustBlockIDFromHexString("0xaaa7bacf26f1aa4754d42edeab45d6169ea723b7fdf0f6ff3b6ebe90d09dbff6bc553936"),
				iotago.MustBlockIDFromHexString("0xba75a143de4ac932986fbe7b1d78f639bc6ee8aee10d510d41572851530be884778052aa"),
				iotago.MustBlockIDFromHexString("0xea5315941f4337752905599710b55e64018c71f4d8f299d0636d50484d05e6ac5667b503"),
			},
		).
		SlotCommitmentID(commitmentID).
		LatestFinalizedSlot(500).
		HighestSupportedVersion(api.ProtocolParameters().Version()).
		ProtocolParametersHash(lo.PanicOnErr(api.ProtocolParameters().Hash())).
		IssuingTime(api.TimeProvider().GenesisTime().Add(30*time.Second)).
		Sign(issuerID, keyPair.PrivateKey[:]).
		Build())
}
