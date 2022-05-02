module TC_Rom (clk, rst, load, save, address, in, out);
    parameter BIT_WIDTH = 16;
    parameter MEM_WORDS = 256;
    parameter HEX_FILE = "test_jumps.mem";
    parameter ARG_SIG = "HEX_FILE=%s";
    reg [1024*8:0] hexfile;
    input clk;
    input rst;
    input load;
    input save;
    input [15:0] address;
    input [BIT_WIDTH-1:0] in;
    output reg [BIT_WIDTH-1:0] out;

    reg [BIT_WIDTH-1:0] mem [0:MEM_WORDS];

    initial begin
        hexfile <= HEX_FILE;
        if ($value$plusargs(ARG_SIG, hexfile)) begin
            $display("loading %0s", hexfile);
            $readmemh(hexfile, mem);
        end else begin
            $display("no file specified");
            for (i=0; i<MEM_WORDS; i=i+1) mem[i] <= {BIT_WIDTH{1'b0}};
        end
        out <= {BIT_WIDTH{1'b0}};
    end

    always @ (address or rst) begin
        if (load && !rst)
            out <= mem[address];
        else
            out <= {BIT_WIDTH{1'b0}};
    end
    always @ (negedge clk) begin
        if (save && !rst)
            mem[address] <= in;
    end
endmodule
