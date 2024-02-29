package examples

import (
	"crypto/ed25519"
	"fmt"
	"math/big"
	"time"

	hiveEd25519 "github.com/iotaledger/hive.go/crypto/ed25519"
	"github.com/iotaledger/hive.go/lo"
	"github.com/iotaledger/iota-crypto-demo/pkg/bip32path"
	"github.com/iotaledger/iota-crypto-demo/pkg/slip10"
	"github.com/iotaledger/iota-crypto-demo/pkg/slip10/eddsa"
	iotago "github.com/iotaledger/iota.go/v4"
	"github.com/iotaledger/iota.go/v4/builder"
	"github.com/iotaledger/iota.go/v4/hexutil"
	"github.com/iotaledger/iota.go/v4/tpkg"
)

var (
	commitmentID = iotago.MustCommitmentIDFromHexString("0x3a1e3b617060146e0362361a4b752833186108395f3b2b3d3e6c655e287d707601000000")
	issuerID     = iotago.MustAccountIDFromHexString("0x17432c5a7a672503480241125e3952414a7a320441080c624c264b004e09614a")
	privateKey   = lo.Return1(hiveEd25519.PrivateKeyFromBytes(lo.PanicOnErr(hexutil.DecodeHex(
		"0x9396e0257e40961ae310777a3d12d3fe1f6811eeb073d169d538d50753c68eb82daefbcbadd044da470acd2f7fcf6fcb04b873cc801e7ee408018e1dfa0257ac",
	))))
	keyPair = hiveEd25519.KeyPair{
		PrivateKey: privateKey,
		PublicKey:  privateKey.Public(),
	}
	addr            = iotago.Ed25519AddressFromPubKey(keyPair.PublicKey[:])
	pubkey1         = lo.PanicOnErr(hexutil.DecodeHex("0x9e05a32eafedefd40298e24ad4f8c334580187f7e9afbd9da13b5ba4007dd1b5"))
	blockIssuerKey1 = iotago.Ed25519PublicKeyHashBlockIssuerKeyFromPublicKey(hiveEd25519.PublicKey(pubkey1))
	pubkey2         = lo.PanicOnErr(hexutil.DecodeHex("0xa504844f7a0df2c5101d31696593b309040f8660d41035aba508f24c00668b21"))
	blockIssuerKey2 = iotago.Ed25519PublicKeyHashBlockIssuerKeyFromPublicKey(hiveEd25519.PublicKey(pubkey2))
	OneIOTA         = iotago.BaseToken(1_000_000)
	OneMana         = iotago.Mana(1_000_000)
)

func SignedTransaction(api iotago.API) *iotago.SignedTransaction {
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
		Amount: 100_000,
		Mana:   5000,
		UnlockConditions: iotago.AccountOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.AccountOutputFeatures{
			&iotago.MetadataFeature{
				Entries: iotago.MetadataFeatureEntries{
					"hello": []byte("world"),
				},
			},
			&iotago.BlockIssuerFeature{
				ExpirySlot:      iotago.MaxSlotIndex,
				BlockIssuerKeys: iotago.NewBlockIssuerKeys(blockIssuerKey1, blockIssuerKey2),
			},
			&iotago.StakingFeature{
				StakedAmount: 10_000,
				FixedCost:    400,
				StartEpoch:   0,
				EndEpoch:     iotago.MaxEpochIndex,
			},
		},
	}

	tx := lo.PanicOnErr(builder.NewTransactionBuilder(api, iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})).
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
		SetCreationSlot(commitmentID.Index() + api.ProtocolParameters().MinCommittableAge()).
		Build())

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
		LatestFinalizedSlot(commitmentID.Index()-1).
		IssuingTime(api.TimeProvider().GenesisTime().Add(120*time.Second)).
		Sign(
			issuerID,
			keyPair.PrivateKey[:],
		).
		Build())
}

func BasicBlockWithoutPayload(api iotago.API) *iotago.Block {
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
		IssuingTime(api.TimeProvider().GenesisTime().Add(120*time.Second)).
		Sign(issuerID, keyPair.PrivateKey[:]).
		Build())
}

func SignedTransactionOutputIdProof(api iotago.API, outputCount uint8) *iotago.SignedTransaction {
	addr := iotago.Ed25519AddressFromPubKey(keyPair.PublicKey[:])
	seed := lo.PanicOnErr(hexutil.DecodeHex("0x394821f8f257e0a502f21ac7ee57530bb9dc29fe12ff3936f925b835a2976804"))
	slip10Path := "44'/4218'/0'/0'/0/%d"

	deriveAddress := func(addressIndex uint8) *iotago.Ed25519Address {
		curve := eddsa.Ed25519()
		path := lo.PanicOnErr(bip32path.ParsePath(fmt.Sprintf(slip10Path, addressIndex)))
		key := lo.PanicOnErr(slip10.DeriveKeyFromPath(seed, curve, path))
		public, _ := key.Key.(eddsa.Seed).Ed25519Key()
		return iotago.Ed25519AddressFromPubKey(ed25519.PublicKey(public))
	}

	tx := builder.NewTransactionBuilder(api, iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      iotago.MustOutputIDFromHexString("0xf09d3cd648a7246c7c1b2ba2f9182465ae5742b78c592392b4b455ab8ed71952000000000000"),
			Input: &iotago.BasicOutput{
				Amount: 1000 * OneIOTA,
			},
		})

	for idx := uint8(0); idx <= outputCount; idx++ {
		tx.AddOutput(
			&iotago.BasicOutput{
				Amount: OneIOTA,
				UnlockConditions: iotago.BasicOutputUnlockConditions{
					&iotago.AddressUnlockCondition{
						Address: deriveAddress(idx),
					},
				},
			},
		)
	}

	signedTx := lo.PanicOnErr(tx.
		WithTransactionCapabilities(
			iotago.TransactionCapabilitiesBitMaskWithCapabilities(iotago.WithTransactionCanDoAnything()),
		).
		SetCreationSlot(commitmentID.Index() + api.ProtocolParameters().MinCommittableAge()).
		Build())

	return signedTx
}

func SignedTransactionOutputMana(api iotago.API) (iotago.OutputID, *iotago.BasicOutput, *iotago.SignedTransaction) {
	// Pick a commitment that is further away from the genesis to properly test mana decay.
	manaCommitmentID := iotago.MustCommitmentIDFromHexString("0x3a1e3b617060146e0362361a4b752833186108395f3b2b3d3e6c655e287d7076364b4c00")
	inputID := iotago.MustOutputIDFromHexString("0xf09d3cd648a7246c7c1b2ba2f9182465ae5742b78c592392b4b455ab8ed71950050000000000")

	input := &iotago.BasicOutput{
		Amount: 100000,
		Mana:   4000,
		UnlockConditions: iotago.BasicOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.BasicOutputFeatures{},
	}
	inputCreationSlot := inputID.Slot()
	txCreationSlot := manaCommitmentID.Index() + api.ProtocolParameters().MinCommittableAge()
	potentialMana := lo.PanicOnErr(iotago.PotentialMana(api.ManaDecayProvider(), api.StorageScoreStructure(), input, inputCreationSlot, txCreationSlot))

	storedMana := lo.PanicOnErr(api.ManaDecayProvider().DecayManaBySlots(input.Mana, inputCreationSlot, txCreationSlot))

	output := &iotago.BasicOutput{
		Amount: 100000,
		Mana:   potentialMana,
		UnlockConditions: iotago.BasicOutputUnlockConditions{
			&iotago.AddressUnlockCondition{
				Address: addr,
			},
		},
		Features: iotago.BasicOutputFeatures{},
	}

	tx := lo.PanicOnErr(builder.NewTransactionBuilder(api, iotago.NewInMemoryAddressSigner(iotago.AddressKeys{Address: addr, Keys: ed25519.PrivateKey(keyPair.PrivateKey[:])})).
		AddInput(&builder.TxInput{
			UnlockTarget: addr,
			InputID:      inputID,
			Input:        input,
		}).
		AddOutput(output).
		AddCommitmentInput(&iotago.CommitmentInput{CommitmentID: manaCommitmentID}).
		IncreaseAllotment(
			iotago.MustAccountIDFromHexString("0x476820096e7038107d071a4e473f1e295f346e2d0824263e5e3e7d004f6b6915"),
			storedMana,
		).
		SetCreationSlot(manaCommitmentID.Index() + api.ProtocolParameters().MinCommittableAge()).
		Build())

	return inputID, input, tx
}

func DelegationOutputStorageScore() *iotago.DelegationOutput {
	validatorAddress := iotago.AccountAddress(issuerID)
	delegationID := iotago.DelegationID(lo.PanicOnErr(hexutil.DecodeHex("0x08b987baffaacb9da156734275ee01a42a35fe06653823be654821a7ddf92380")))

	delegationOutput := builder.NewDelegationOutputBuilder(
		&validatorAddress,
		addr,
		200*OneIOTA,
	).
		StartEpoch(30).
		EndEpoch(50).
		DelegatedAmount(500 * OneIOTA).
		DelegationID(delegationID).
		MustBuild()

	return delegationOutput
}

func BasicOutputStorageScore() *iotago.BasicOutput {
	nativeTokenID := iotago.NativeTokenID(lo.PanicOnErr(hexutil.DecodeHex("0x083ef5555d65ba314fb1680147da0d54b08cecfd9a728bdcf5f1ebda1fedb9f852435d8d1000")))

	basicOutput := builder.NewBasicOutputBuilder(
		addr,
		200*OneIOTA,
	).
		Mana(555 * OneMana).
		Tag([]byte("storage_score")).
		Metadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.0"),
		}).
		Timelock(999).
		NativeToken(&iotago.NativeTokenFeature{
			ID:     nativeTokenID,
			Amount: big.NewInt(42),
		}).
		MustBuild()

	return basicOutput
}

func AccountOutputStorageScore() *iotago.AccountOutput {
	accountID := iotago.MustAccountIDFromHexString("0xe8494fe353f99783d3771c78798e1e839e649310513770fc6dc974fe53cf1a86")

	accountOutput := builder.NewAccountOutputBuilder(
		addr,
		200*OneIOTA,
	).
		Mana(333*OneMana).
		AccountID(accountID).
		ImmutableMetadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.0"),
		}).
		BlockIssuer(iotago.NewBlockIssuerKeys(
			blockIssuerKey1,
			blockIssuerKey2,
		), 888).
		Sender(addr).
		Staking(150*OneIOTA, 400, 25, iotago.MaxEpochIndex).
		MustBuild()

	return accountOutput
}

func NFTOutputStorageScore() *iotago.NFTOutput {
	accountAddress := iotago.AccountAddress(issuerID)

	nftOutput := builder.NewNFTOutputBuilder(
		&accountAddress,
		421*OneIOTA,
	).
		Metadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.0"),
		}).
		StorageDepositReturn(addr, 4*OneIOTA).
		ImmutableMetadata(iotago.MetadataFeatureEntries{
			"nft": []byte("iota"),
		}).
		NFTID(tpkg.RandNFTID()).
		MustBuild()

	return nftOutput
}

func FoundryOutputStorageScore() *iotago.FoundryOutput {
	accountAddress := iotago.AccountAddress(issuerID)
	serialNumber := uint32(1)
	tokenScheme := &iotago.SimpleTokenScheme{
		MintedTokens:  big.NewInt(40000),
		MeltedTokens:  big.NewInt(10000),
		MaximumSupply: big.NewInt(50000),
	}

	nativeTokenID := lo.PanicOnErr(iotago.FoundryIDFromAddressAndSerialNumberAndTokenScheme(&accountAddress, serialNumber, tokenScheme.Type()))

	foundryOutput := builder.NewFoundryOutputBuilder(
		&accountAddress,
		420*OneIOTA,
		serialNumber,
		tokenScheme,
	).
		Metadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.00000000000000000000000000000000000000000000"),
		}).
		NativeToken(&iotago.NativeTokenFeature{
			ID:     nativeTokenID,
			Amount: big.NewInt(42000),
		}).
		MustBuild()

	return foundryOutput
}

func AnchorOutputStorageScore() *iotago.AnchorOutput {
	accountAddress := iotago.AccountAddress(issuerID)

	anchorOutput := builder.NewAnchorOutputBuilder(
		&accountAddress,
		&accountAddress,
		420*OneIOTA,
	).
		Metadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.0"),
		}).
		ImmutableMetadata(iotago.MetadataFeatureEntries{
			"iota": []byte("2.0"),
		}).
		Mana(42).
		MustBuild()

	return anchorOutput
}
