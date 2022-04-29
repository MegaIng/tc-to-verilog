module TC_CheapRamLat (clk, rst, load, save, address, in0, in1, in2, in3, ready, out0, out1, out2, out3);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 65536;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in0;
    input [BIT_WIDTH-1:0] in1;
    input [BIT_WIDTH-1:0] in2;
    input [BIT_WIDTH-1:0] in3;
    output tri0 ready;
    output tri0 [BIT_WIDTH-1:0] out0;
    output tri0 [BIT_WIDTH-1:0] out1;
    output tri0 [BIT_WIDTH-1:0] out2;
    output tri0 [BIT_WIDTH-1:0] out3;
    reg readywait;
    reg readyval;
    reg [BIT_WIDTH-1:0] outwait0;
    reg [BIT_WIDTH-1:0] outwait1;
    reg [BIT_WIDTH-1:0] outwait2;
    reg [BIT_WIDTH-1:0] outwait3;
    reg [BIT_WIDTH-1:0] outval0;
    reg [BIT_WIDTH-1:0] outval1;
    reg [BIT_WIDTH-1:0] outval2;
    reg [BIT_WIDTH-1:0] outval3;
    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];
    always @ (posedge clk or rst) begin
        outval0 <= outwait0;
        outval1 <= outwait1;
        outval2 <= outwait2;
        outval3 <= outwait3;
        readyval <= readywait;
        if (load && !rst) begin
            outwait0 <= mem[address];
            outwait1 <= mem[address+1];
            outwait2 <= mem[address+2];
            outwait3 <= mem[address+3];
            readywait <= 1'b1;
        end else begin
            outwait0 <= {BIT_WIDTH{1'bZ}};
            outwait1 <= {BIT_WIDTH{1'bZ}};
            outwait2 <= {BIT_WIDTH{1'bZ}};
            outwait3 <= {BIT_WIDTH{1'bZ}};
            readywait <= 1'bZ;
        end
    end
    always @ (negedge clk) begin
        if (save) begin
            mem[address] <= in0;
            mem[address+1] <= in1;
            mem[address+2] <= in2;
            mem[address+3] <= in3;
        end
    end
    assign out0 = outval0;
    assign out1 = outval1;
    assign out2 = outval2;
    assign out3 = outval3;
    assign ready = readyval;
endmodule
