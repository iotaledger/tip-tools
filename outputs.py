# -*- coding: utf-8 -*-

#===============================================================================
# returns the maximum possible size of a payload
def getPayloadSizeMax(message_size_max):
    payload_size_max = message_size_max
    payload_size_max -= 8               # NetworkID
    payload_size_max -= 1               # ParentCount
    payload_size_max -= 32              # Parent
    payload_size_max -= 4               # PayloadLength
                                        # Placeholder for Payload
    payload_size_max -= 8               # Nonce
    
    return payload_size_max

#===============================================================================
# returns the maximum possible size of an output
def getOutputSizeMax(transaction_size_max, inputs=1):
    output_size_max = transaction_size_max
    output_size_max -= 4                # Payload Type
    output_size_max -= 1                # Transaction Type
    output_size_max -= 2                # Inputs Count
    for i in range(inputs):
        output_size_max -= (1+32+2)     # 1x UTXO Input (Input Type + Transaction ID + Transaction Output Index)
    output_size_max -= 2                # Outputs Count
                                        # Placeholder for Outputs
    output_size_max -= 4                # Payload Length
                                        # Placeholder for Payload
    output_size_max -= 2                # Unlock Blocks Count
    for i in range(inputs):
        output_size_max -= (1+1+32+64)  # 1x Unlock Blocks (Unlock Type - Signature Type + Public key + Signature)    
    
    return output_size_max

#===============================================================================
class Output_VBytes(object):
    #---------------------------------------------------------------------------
    def __init__(self, name, name_plot, max_byte_size, plot_row_index=0, plot_column_index=0):
        self.name               = name
        self.name_plot          = name_plot
        self.max_byte_size      = max_byte_size     # maximum available bytes

        self.plot_row_index     = plot_row_index
        self.plot_column_index  = plot_column_index 
        
        self.byte_size_max      = 0                 # currently used bytes max
        self.v_bytes_min        = 0
        self.v_bytes_max        = 0 

        self.plot_y_values      = []

    #---------------------------------------------------------------------------
    def summary(self):
        print("Name: %s, v_byte_min: %d, v_byte_max: %d" % (self.name, self.v_bytes_min, self.v_bytes_max))
    
    #---------------------------------------------------------------------------
    def addField(self, field_byte_size_min, field_byte_size_max, weight):
        self.byte_size_max   += field_byte_size_max
        if self.byte_size_max > self.max_byte_size:
            raise Exception("Output too big: %s, Current: %d, Max: %d" % (self.name, self.byte_size_max, self.max_byte_size))
        self.v_bytes_min += field_byte_size_min*weight 
        self.v_bytes_max += field_byte_size_max*weight 

    #---------------------------------------------------------------------------
    def byteSizeMax(self):
        return self.byte_size_max

    #---------------------------------------------------------------------------
    def bytesRemaining(self):
        return self.max_byte_size - self.byte_size_max

    #---------------------------------------------------------------------------
    def vBytesMin(self):
        return self.v_bytes_min

    #---------------------------------------------------------------------------
    def vBytesMax(self):
        return self.v_bytes_max

    #---------------------------------------------------------------------------
    def totalOutputsPossible(self, db_size_bytes_max):
        return int(db_size_bytes_max / self.byte_size_max)

#===============================================================================
def getVBytes_Byte():

    vbytes = Output_VBytes(name="byte", name_plot="byte", max_byte_size=1)
    vbytes.addField(field_byte_size_min=1,  field_byte_size_max=1, weight=1.0)
    
    return vbytes

#===============================================================================
def getVBytes_SimpleOutput(weight_key,
                           weight_data,
                           additional_name,
                           output_size_max):

    name        = "SimpleOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name=name, name_plot=name_plot, max_byte_size=output_size_max)
    vbytes.addField(field_byte_size_min=34,  field_byte_size_max=34, weight=weight_key)                  # Output ID
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                 # Output Type
    vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                 # Amount
    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_key+weight_data)      # Address

    return vbytes

#===============================================================================
def getVBytes_ExtendedOutput(weight_key,
                             weight_data,
                             additional_name,
                             output_size_max,
                             native_token_count, 
                             sender_block=True,
                             return_amount_block=True,
                             timelock_ms_idx_block=True,
                             timelock_unix_block=True,
                             expiration_ms_idx_block=True,
                             expiration_unix_block=True,
                             indexation_block=True,
                             metadata_block=True):

    name        = "ExtendedOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name=name, name_plot=name_plot, max_byte_size=output_size_max)

    vbytes.addField(field_byte_size_min=34,  field_byte_size_max=34, weight=weight_key)                                         # Output ID
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                        # Output Type
    vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                        # Amount
    vbytes.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=weight_data)                                        # Native Tokens Count
    
    for i in range(native_token_count):
        vbytes.addField(field_byte_size_min=38+32,  field_byte_size_max=38+32, weight=weight_data)                              # Native Tokens (TokenID+Amount)
    
    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_key+weight_data)                             # Address

    # Sender Block
    if sender_block:
        multiplier = 1
        if indexation_block:
            multiplier = 2
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=multiplier*(weight_key+weight_data))            # Sender

    # Return Amount Block
    if return_amount_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                    # Return Amount

    # Timelock Milestone Index Block
    if timelock_ms_idx_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Milestone Index

    # Timelock Unix Block
    if timelock_unix_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Unix Time

    # Expiration Milestone Index Block
    if expiration_ms_idx_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Milestone Index

    # Expiration Unix Block
    if expiration_unix_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Unix Time

    # Indexation Block
    if indexation_block:
        multiplier = 1
        if sender_block:
            multiplier = 2
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Indexation Data Length
        vbytes.addField(field_byte_size_min=64,  field_byte_size_max=64, weight=multiplier*(weight_key+weight_data))            # Indexation Data

    # Metadata Block
    if metadata_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Metadata Data Length
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=vbytes.bytesRemaining(), weight=weight_data)               # Metadata Data (we can just use the remaining size here since every other dynamic field has the same weight)

    return vbytes

#===============================================================================
def getVBytes_AliasOutput(weight_key,
                          weight_data,
                          additional_name,
                          output_size_max,
                          native_token_count, 
                          metadata_block=True):

    name        = "AliasOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name=name, name_plot=name_plot, max_byte_size=output_size_max)

    vbytes.addField(field_byte_size_min=34,  field_byte_size_max=34, weight=weight_key)                                         # Output ID
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                        # Output Type
    vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                        # Amount
    vbytes.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=weight_data)                                        # Native Tokens Count
    
    for i in range(native_token_count):
        vbytes.addField(field_byte_size_min=38+32,  field_byte_size_max=38+32, weight=weight_data)                              # Native Tokens (TokenID+Amount)

    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=21, weight=weight_key+weight_data)                             # Alias ID
    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_key+weight_data)                             # State Controller
    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_key+weight_data)                             # Governance Controller
    vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                        # State Index
    vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                        # State Metadata Length
    vbytes.addField(field_byte_size_min=0,   field_byte_size_max=0,  weight=weight_data)                                        # State Metadata (zero for now, the remaining space will be taken into account in the metadata block)
    vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                        # Foundry Counter

    # Metadata Block
    if metadata_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Metadata Data Length
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=output_size_max-vbytes.byteSizeMax(), weight=weight_data)  # Metadata Data (we can just use the remaining size here since every other dynamic field has the same weight)

    return vbytes

#===============================================================================
def getVBytes_FoundryOutput(weight_key,
                            weight_data,
                            additional_name,
                            output_size_max,
                            native_token_count, 
                            metadata_block=True):

    name        = "FoundryOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name=name, name_plot=name_plot, max_byte_size=output_size_max)

    vbytes.addField(field_byte_size_min=34,  field_byte_size_max=34, weight=weight_key)                                         # Output ID
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                        # Output Type
    vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                        # Amount
    vbytes.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=weight_data)                                        # Native Tokens Count
    
    for i in range(native_token_count):
        vbytes.addField(field_byte_size_min=38+32,  field_byte_size_max=38+32, weight=weight_data)                              # Native Tokens (TokenID+Amount)

    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=21, weight=weight_key+weight_data)                             # Address
    vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_key+weight_data)                             # SerialNumber

    vbytes.addField(field_byte_size_min=12,  field_byte_size_max=12, weight=weight_data)                                        # Token Tag
    vbytes.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=weight_data)                                        # Circulating Supply
    vbytes.addField(field_byte_size_min=32,  field_byte_size_max=32, weight=weight_data)                                        # Maximum Supply
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_key+weight_data)                             # Token Scheme

    # Metadata Block
    if metadata_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Metadata Data Length
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=vbytes.bytesRemaining(), weight=weight_data)               # Metadata Data (we can just use the remaining size here since every other dynamic field has the same weight)

    return vbytes

#===============================================================================
def getVBytes_NFTOutput(weight_key,
                        weight_data,
                        additional_name,
                        output_size_max,
                        native_token_count, 
                        sender_block=True,
                        issuer_block=True,
                        return_amount_block=True,
                        timelock_ms_idx_block=True,
                        timelock_unix_block=True,
                        expiration_ms_idx_block=True,
                        expiration_unix_block=True,
                        indexation_block=True,
                        metadata_block=True):

    name        = "NFTOutput"
    name_plot   = name
    if additional_name != None:
        name        = "%s (%s)" %  (name, additional_name)
        name_plot   = "%s\n(%s)" % (name_plot, additional_name)
    
    vbytes = Output_VBytes(name=name, name_plot=name_plot, max_byte_size=output_size_max)

    vbytes.addField(field_byte_size_min=34,  field_byte_size_max=34, weight=weight_key)                                         # Output ID
    vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                        # Output Type
    vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                        # Amount
    vbytes.addField(field_byte_size_min=2,   field_byte_size_max=2,  weight=weight_data)                                        # Native Tokens Count
    
    for i in range(native_token_count):
        vbytes.addField(field_byte_size_min=38+32,  field_byte_size_max=38+32, weight=weight_data)                              # Native Tokens (TokenID+Amount)

    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_key+weight_data)                             # Address
    vbytes.addField(field_byte_size_min=21,  field_byte_size_max=21, weight=weight_key+weight_data)                             # NFT ID
    vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                        # Immutable Metadata Length
    vbytes.addField(field_byte_size_min=0,   field_byte_size_max=0,  weight=weight_data)                                        # Immutable Metadata (zero for now, the remaining space will be taken into account in the metadata block)

    # Sender Block
    if sender_block:
        multiplier = 1
        if indexation_block:
            multiplier = 2
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=multiplier*(weight_key+weight_data))            # Sender

    # Issuer Block
    if issuer_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=21,  field_byte_size_max=33, weight=weight_data)                                    # Issuer

    # Return Amount Block
    if return_amount_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=8,   field_byte_size_max=8,  weight=weight_data)                                    # Return Amount

    # Timelock Milestone Index Block
    if timelock_ms_idx_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Milestone Index

    # Timelock Unix Block
    if timelock_unix_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Unix Time

    # Expiration Milestone Index Block
    if expiration_ms_idx_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Milestone Index

    # Expiration Unix Block
    if expiration_unix_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Unix Time

    # Indexation Block
    if indexation_block:
        multiplier = 1
        if sender_block:
            multiplier = 2
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Indexation Data Length
        vbytes.addField(field_byte_size_min=64,  field_byte_size_max=64, weight=multiplier*(weight_key+weight_data))            # Indexation Data

    # Metadata Block
    if metadata_block:
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=1,  weight=weight_data)                                    # Block Type
        vbytes.addField(field_byte_size_min=4,   field_byte_size_max=4,  weight=weight_data)                                    # Metadata Data Length
        vbytes.addField(field_byte_size_min=1,   field_byte_size_max=vbytes.bytesRemaining(), weight=weight_data)               # Metadata Data (we can just use the remaining size here since every other dynamic field has the same weight)

    return vbytes

#===============================================================================
if __name__ == '__main__':
    MSG_SIZE_MAX        = 32768
    WEIGHT_KEY          = 10.0
    WEIGHT_DATA         = 1.0
    payload_size_max    = getPayloadSizeMax(message_size_max=MSG_SIZE_MAX)
    output_size_max     = getOutputSizeMax(transaction_size_max=payload_size_max, inputs=1)
    
    print("MessageSizeMax: %d" % (MSG_SIZE_MAX))
    print("PayloadSizeMax: %d" % (payload_size_max))
    print("OutputSizeMax: %d" % (output_size_max))

    for vbytes in [getVBytes_SimpleOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name=None,
                        output_size_max=output_size_max,
                   ), 
                   getVBytes_ExtendedOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="min functionality",
                        output_size_max=output_size_max,
                        native_token_count=0, 
                        sender_block=False,
                        return_amount_block=False,
                        timelock_ms_idx_block=False,
                        timelock_unix_block=False,
                        expiration_ms_idx_block=False,
                        expiration_unix_block=False,
                        indexation_block=False,
                        metadata_block=False,
                   ),
                   getVBytes_ExtendedOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="max functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        sender_block=True,
                        return_amount_block=True,
                        timelock_ms_idx_block=True,
                        timelock_unix_block=True,
                        expiration_ms_idx_block=True,
                        expiration_unix_block=True,
                        indexation_block=True,
                        metadata_block=True,
                   ),
                   getVBytes_AliasOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="min functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        metadata_block=False),
                   getVBytes_AliasOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="max functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        metadata_block=True),
                   getVBytes_FoundryOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="min functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        metadata_block=False),
                   getVBytes_FoundryOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="max functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        metadata_block=True),
                   getVBytes_NFTOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="min functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        sender_block=False,
                        issuer_block=False,
                        return_amount_block=False,
                        timelock_ms_idx_block=False,
                        timelock_unix_block=False,
                        expiration_ms_idx_block=False,
                        expiration_unix_block=False,
                        indexation_block=False,
                        metadata_block=False),
                   getVBytes_NFTOutput(
                        weight_key=WEIGHT_KEY,
                        weight_data=WEIGHT_DATA,
                        additional_name="max functionality",
                        output_size_max=output_size_max,
                        native_token_count=0,
                        sender_block=True,
                        issuer_block=True,
                        return_amount_block=True,
                        timelock_ms_idx_block=True,
                        timelock_unix_block=True,
                        expiration_ms_idx_block=True,
                        expiration_unix_block=True,
                        indexation_block=True,
                        metadata_block=True)
    ]:
        vbytes.summary()
